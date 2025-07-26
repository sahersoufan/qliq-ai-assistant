import json
from pathlib import Path

from langchain_community.vectorstores import Chroma

from domain.services.embedding_formatter import gig_to_text
from infrastructure.vector_db.vector_store_builder import build_chroma_store

DATA_PATH = Path(__file__).resolve().parents[2] / "data"
CHROMA_PATH = Path("chroma_db/gigs")
COLLECTION_NAME = "qliq-gigs"

import shutil

if CHROMA_PATH.exists():
    shutil.rmtree(CHROMA_PATH)

def load_gigs() -> list[dict]:
    path = DATA_PATH / "gigs.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_gig_store() -> Chroma:
    items = load_gigs()
    return build_chroma_store(items, gig_to_text, COLLECTION_NAME, CHROMA_PATH)
