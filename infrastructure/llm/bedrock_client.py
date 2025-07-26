# infrastructure/llm/bedrock_client.py
import os

from dotenv import load_dotenv
from langchain_aws.chat_models.bedrock import ChatBedrock
from langchain_core.messages import HumanMessage

load_dotenv()

def get_bedrock_llm():
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2")

    # Initialize LangChain's BedrockChat model
    llm = ChatBedrock(
        model=model_id,
        region=region,
        model_kwargs={
            "max_tokens": 300,
            "temperature": 0.7
        },
        beta_use_converse_api=True
    )

    return llm


def invoke_bedrock(text: str) -> str:
    llm = get_bedrock_llm()
    response = llm.invoke([HumanMessage(content=text)])
    return response.content
