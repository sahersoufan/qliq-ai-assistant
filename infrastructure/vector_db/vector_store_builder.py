from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

from domain.utils.metadata_cleaner import clean_metadata


def build_chroma_store(items: list[dict], to_text_fn, collection_name: str, storage_path: Path) -> Chroma:
    texts = [to_text_fn(item) for item in items]
    documents = [
        Document(
            page_content=text,
            metadata=clean_metadata({"id": item["id"], **item})
        )
        for text, item in zip(texts, items)
    ]

    embedding_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_fn,
        persist_directory=str(storage_path),
        collection_name=collection_name
    )

    print(f"✅ Stored {len(items)} documents to Chroma at {storage_path}")
    return store
