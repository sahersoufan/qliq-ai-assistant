# domain/services/audit_service.py
from datetime import datetime
from infrastructure.logging import logger

def log_activity(user_id, action, details=None):
    """Simple audit logging function"""
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details or {}
    }
    logger.info(f"AUDIT: {action}", **audit_data)