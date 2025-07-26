# domain/services/onboarding_service.py
import json
import traceback

from langchain.agents import create_tool_calling_agent
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

from infrastructure.llm.bedrock_client import get_bedrock_llm, invoke_bedrock
from infrastructure.utils.content_filter import is_clean_text, sanitize_text


class OnboardingService:
    def __init__(self):
        self.llm = get_bedrock_llm()
        self.memory = ConversationBufferWindowMemory(k=3, return_messages=True, memory_key="history")

        self.tools = [
            Tool(
                name="GenerateUserSummary",
                func=self.get_summary,
                description="Use this tool to generate a welcome summary when the user's role, interests, and goals are known. Requires: name, type, interests, goals.",
                return_direct=True
            )

        ]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an onboarding assistant. Greet users and ask their role, interests, and goals. When all are collected, call the tool GenerateUserSummary."),
            ("system", "{history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
        )

    def chat(self, user_input: str) -> str:
        if not is_clean_text(user_input):
            return "Let’s keep things respectful. Could you rephrase that?"

        try:
            response = self.executor.invoke({"input": user_input})
        except Exception as e:
            traceback.print_exc()
            return f"Something went wrong while processing: {str(e)}"

        output = response.get("output", "")

        if not is_clean_text(output):
            return "Let’s continue respectfully. Could you tell me more politely?"

        return sanitize_text(output)

    def get_summary(self, user_profile: dict) -> str:
        user_profile = json.loads(str(user_profile))

        name = user_profile.get("name", "there")
        role = user_profile.get("type", "a user")
        interests = ", ".join(user_profile.get("interests", []))
        goals = ", ".join(user_profile.get("goals", []))

        summary_prompt = (
            f"Generate a short welcome message for {name}. "
            f"They're a {role} interested in {interests} with goals like {goals}."
        )

        return sanitize_text(invoke_bedrock(summary_prompt))
