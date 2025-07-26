# infrastructure/vector_db/chroma_client.py

import json
from pathlib import Path

from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

from domain.utils.metadata_cleaner import clean_metadata

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data"
CHROMA_PATH = BASE_DIR / "app" / "chroma_db"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


def _save_collection(documents: list[Document], collection_name: str):
    embeddings = SentenceTransformerEmbeddings(model_name=EMBED_MODEL_NAME)
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH),
        collection_name=collection_name
    )
    print(f"Saved collection '{collection_name}' with {len(documents)} documents.")


def build_all_collections():
    _save_collection(load_gig_documents(), "gigs")
    _save_collection(load_product_documents(), "products")
    _save_collection(load_faq_documents(), "faqs")
    _save_collection(load_user_documents(), "users")  # optional: not used directly yet


def _load_collection(collection_name: str):
    embeddings = SentenceTransformerEmbeddings(model_name=EMBED_MODEL_NAME)
    return Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
        collection_name=collection_name
    )


def load_gig_retriever():
    return _load_collection("gigs").as_retriever()


def load_product_retriever():
    return _load_collection("products").as_retriever()


def load_faq_retriever():
    return _load_collection("faqs").as_retriever()


def load_general_retriever():
    return _load_collection("gigs").as_retriever()  # fallback for now


# Individual loaders for each data type
def load_gig_documents():
    path = DATA_PATH / "gigs.json"
    documents = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                content = f"""Gig Title: {item.get("title")}
Category: {item.get("category")}
Description: {item.get("description")}
Skills Required: {", ".join(item.get("skills_required", []))}"""
                documents.append(Document(
                    page_content=content.strip(),
                    metadata=clean_metadata({"source": "gigs", **item})
                ))
    return documents


def load_product_documents():
    path = DATA_PATH / "products.json"
    documents = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                content = f"""Product Name: {item.get("name")}
Category: {item.get("category")}
Description: {item.get("description")}
Price: ${item.get("price")}
Seller Type: {item.get("seller_type")}"""
                documents.append(Document(
                    page_content=content.strip(),
                    metadata=clean_metadata({"source": "products", **item})
                ))
    return documents


def load_user_documents():
    path = DATA_PATH / "users.json"
    documents = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                interests = ", ".join(item.get("interests", []))
                goals = ", ".join(item.get("goals", []))
                content = f"""User Name: {item.get("name")}
Type: {item.get("type")}
Interests: {interests}
Goals: {goals}
Location: {item.get("location")}
Qoyns Balance: {item.get("qoyns_balance")}
Network Size: {item.get("network_size")}"""
                documents.append(Document(
                    page_content=content.strip(),
                    metadata=clean_metadata({"source": "users", **item})
                ))
    return documents


def load_platform_doc_documents():
    path = DATA_PATH / "platform_docs.json"
    documents = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                content = f"""Platform Document Title: {item.get("title")}
Category: {item.get("category")}
Content: {item.get("content")}"""
                documents.append(Document(
                    page_content=content.strip(),
                    metadata=clean_metadata({"source": "platform_docs", **item})
                ))
    return documents


def load_user_guide_documents():
    path = DATA_PATH / "user_guides.json"
    documents = []
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                content = f"""User Guide Title: {item.get("title")}
Category: {item.get("category")}
Content: {item.get("content")}"""
                documents.append(Document(
                    page_content=content.strip(),
                    metadata=clean_metadata({"source": "user_guides", **item})
                ))
    return documents


def load_faq_documents():
    return load_platform_doc_documents() + load_user_guide_documents()
