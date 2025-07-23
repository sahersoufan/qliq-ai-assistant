# interface/api/health.py
from fastapi import APIRouter
from infrastructure.logging import logger
router = APIRouter()

@router.get("/")
def health_check():
    logger.info("QLIQ AI Assistant Health Check")
    return {"status": "ok"}
