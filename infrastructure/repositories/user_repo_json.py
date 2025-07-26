import json
from pathlib import Path
from json.decoder import JSONDecodeError
from infrastructure.logging import logger

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "users.json"

def load_user_by_id(user_id: str) -> dict | None:
    try:
        if not DATA_PATH.exists():
            logger.warning(f"User data file not found at {DATA_PATH}")
            return None
        
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            try:
                users = json.load(f)
                user = next((user for user in users if user.get("id") == user_id), None)
                if user is None:
                    logger.info(f"User with ID {user_id} not found")
                return user
            except JSONDecodeError as e:
                logger.error(f"Failed to parse users JSON: {str(e)}")
                return None
    except PermissionError as e:
        logger.error(f"Permission denied when accessing {DATA_PATH}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading user {user_id}: {str(e)}")
        return None
