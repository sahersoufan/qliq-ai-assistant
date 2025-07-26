import json
from pathlib import Path

from langchain_community.vectorstores import Chroma

from domain.services.embedding_formatter import user_to_text
from infrastructure.vector_db.vector_store_builder import build_chroma_store

DATA_PATH = Path(__file__).resolve().parents[2] / "data"
CHROMA_PATH = Path("chroma_db/users")
COLLECTION_NAME = "qliq-users"

import shutil

if CHROMA_PATH.exists():
    shutil.rmtree(CHROMA_PATH)

def load_users() -> list[dict]:
    path = DATA_PATH / "users.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_user_store() -> Chroma:
    items = load_users()
    return build_chroma_store(items, user_to_text, COLLECTION_NAME, CHROMA_PATH)
