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
from infrastructure.logging import logger


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
        try:
            self.llm = get_bedrock_llm()
            self.classifier = classifier
            
            # Initialize retrievers with error handling
            self.retrievers = {}
            try:
                self.retrievers["FAQ"] = load_faq_retriever()
                logger.info("FAQ retriever loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load FAQ retriever: {str(e)}")
                
            try:
                self.retrievers["Product"] = load_product_retriever()
                logger.info("Product retriever loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Product retriever: {str(e)}")
                
            try:
                self.retrievers["Gig"] = load_gig_retriever()
                logger.info("Gig retriever loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Gig retriever: {str(e)}")
                
            # Initialize general chain
            try:
                self.general_chain = LLMChain(
                    llm=self.llm,
                    prompt=PromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)
                )
                logger.info("General chain initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize general chain: {str(e)}")
                raise RuntimeError(f"Failed to initialize general chain: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error initializing QueryService: {str(e)}")
            raise

    def ask(self, question: str) -> str:
        if not question or not isinstance(question, str):
            logger.warning(f"Invalid question input: {question}")
            return "I couldn't understand your question. Please try again with a clear question."
            
        try:
            # Get classification label
            try:
                label = self.classifier.predict(question)
                logger.info(f"Query classified as: {label}")
            except Exception as e:
                logger.error(f"Error classifying query: {str(e)}")
                label = "General"  # Default to general if classification fails
                
            # Handle general queries
            if label == "General":
                try:
                    result = self.general_chain.run({"question": question})
                    return result
                except Exception as e:
                    logger.error(f"Error processing general query: {str(e)}")
                    return "I'm having trouble processing your request. Please try again later."

            # Get appropriate retriever
            retriever = self.retrievers.get(label)
            if not retriever:
                logger.error(f"No retriever found for label: {label}")
                return "I'm having trouble finding information on that topic. Please try a different question."

            # Create and run QA chain
            try:
                qa_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    condense_question_prompt=PromptTemplate.from_template(QA_TEMPLATE),
                    combine_docs_chain_kwargs={"prompt": PromptTemplate.from_template(QA_TEMPLATE)},
                    return_source_documents=True
                )
                
                result = qa_chain({"question": question, "chat_history": []})
                
                # Log retrieved chunks for debugging
                chunks = [doc.page_content for doc in result["source_documents"]]
                logger.debug(f"Retrieved {len(chunks)} chunks for query")
                
                return result.get("answer", "I'm not sure based on the available information.")
            except Exception as e:
                logger.error(f"Error in QA chain: {str(e)}")
                return "I encountered an issue while searching for your answer. Please try again later."
                
        except Exception as e:
            logger.error(f"Unexpected error processing query: {str(e)}")
            return "I'm sorry, something went wrong. Please try again later."
