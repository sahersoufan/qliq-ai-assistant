import json
from pathlib import Path
from pprint import pprint

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from domain.services.embedding_formatter import product_to_text
from infrastructure.vector_db.vector_store_builder import build_chroma_store

DATA_PATH = Path(__file__).resolve().parents[2] / "data"
CHROMA_PATH = Path("chroma_db/products")
COLLECTION_NAME = "qliq-products"

import shutil

if CHROMA_PATH.exists():
    shutil.rmtree(CHROMA_PATH)


def load_products() -> list[dict]:
    path = DATA_PATH / "products.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_product_store() -> Chroma:
    items = load_products()
    return build_chroma_store(items, product_to_text, COLLECTION_NAME, CHROMA_PATH)


# ✅ Test block for duplicate result check
if __name__ == "__main__":
    print("Building product store and checking for duplicates...")
    store = build_product_store()

    retriever = store.as_retriever()
    query = "Buyer interested in food, gaming, fashion, tech aiming to ['Physical operation land.']"
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    user_vector = embedder.embed_documents([query])[0]

    results = store.similarity_search_by_vector(user_vector, 5)

    print(f"\n🔍 Retrieved {len(results)} documents:")
    pprint(results)

    # ✅ Check for duplicates
    seen = set()
    duplicates = []
    for doc in results:
        doc_id = doc.metadata.get("id")
        if doc_id in seen:
            duplicates.append(doc_id)
        seen.add(doc_id)

    if duplicates:
        print(f"\n🚨 Duplicated product IDs found: {duplicates}")
    else:
        print("\n✅ No duplicate products returned.")
