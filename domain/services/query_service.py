# domain/services/query_service.py

from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from infrastructure.llm.bedrock_client import get_bedrock_llm
from infrastructure.vector_db.chroma_client import load_chroma


QA_TEMPLATE = """
You are a helpful assistant for the QLIQ platform.

Answer the user's question using ONLY the context provided below. If you cannot find a relevant answer in the context, say: "I don't know based on the current documents."

You must use specific information (lists, details, or descriptions) directly from the context if it exists.

Context:
{context}

Question:
{question}
"""


class QueryService:
    def __init__(self):
        retriever = load_chroma().as_retriever()
        llm = get_bedrock_llm()

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            condense_question_prompt=PromptTemplate.from_template(QA_TEMPLATE),
            combine_docs_chain_kwargs={"prompt": PromptTemplate.from_template(QA_TEMPLATE)},
            return_source_documents=True
        )

    def ask(self, question: str) -> str:
        result = self.qa_chain({"question": question, "chat_history": []})
        print("RETRIEVED CHUNKS:\n", [doc.page_content for doc in result["source_documents"]])
        return result.get("answer", "I'm not sure based on the available information.")
