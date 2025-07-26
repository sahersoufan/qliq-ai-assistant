# domain/services/query_service.py

from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from infrastructure.llm.bedrock_client import get_bedrock_llm
from infrastructure.vector_db.chroma_client import (
    load_faq_retriever,
    load_product_retriever,
    load_gig_retriever,
)
from domain.services.query_classifier_service import QueryClassifierService


QA_TEMPLATE = """
You are a helpful assistant for the QLIQ platform.

Answer the user's question using ONLY the context provided below. If you cannot find a relevant answer in the context, say: "I don't know based on the current documents."

You must use specific information (lists, details, or descriptions) directly from the context if it exists.

Context:
{context}

Question:
{question}
"""

GENERAL_PROMPT_TEMPLATE = """
You are an assistant for the QLIQ platform.
The user asked something that is not related to the platform features, products, or gigs.
Politely respond without answering the unrelated query directly. Instead, guide the user to ask about topics you can help with such as:
- Platform usage
- Finding products
- Exploring gig opportunities

User message:
{question}
"""


class QueryService:
    def __init__(self, classifier: QueryClassifierService):
        self.llm = get_bedrock_llm()
        self.classifier = classifier
        self.retrievers = {
            "FAQ": load_faq_retriever(),
            "Product": load_product_retriever(),
            "Gig": load_gig_retriever(),
        }
        self.general_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)
        )

    def ask(self, question: str) -> str:
        label = self.classifier.predict(question)
        print(label)
        if label == "General":
            result = self.general_chain.run({"question": question})
            return result

        retriever = self.retrievers.get(label)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            condense_question_prompt=PromptTemplate.from_template(QA_TEMPLATE),
            combine_docs_chain_kwargs={"prompt": PromptTemplate.from_template(QA_TEMPLATE)},
            return_source_documents=True
        )

        result = qa_chain({"question": question, "chat_history": []})
        print("RETRIEVED CHUNKS:\n", [doc.page_content for doc in result["source_documents"]])
        return result.get("answer", "I'm not sure based on the available information.")
