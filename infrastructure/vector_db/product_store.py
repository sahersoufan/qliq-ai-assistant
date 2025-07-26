import json
from pathlib import Path

from langchain_community.vectorstores import Chroma

from domain.services.embedding_formatter import product_to_text
from infrastructure.vector_db.vector_store_builder import build_chroma_store

DATA_PATH = Path(__file__).resolve().parents[2] / "data"
CHROMA_PATH = Path("chroma_db/products")
COLLECTION_NAME = "qliq-products"


def load_products() -> list[dict]:
    path = DATA_PATH / "products.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_product_store() -> Chroma:
    items = load_products()
    return build_chroma_store(items, product_to_text, COLLECTION_NAME, CHROMA_PATH)
