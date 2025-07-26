import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "users.json"

def load_user_by_id(user_id: str) -> dict | None:
    if not DATA_PATH.exists():
        return None
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)
        return next((user for user in users if user.get("id") == user_id), None)
