# interface/api/metrics.py
from fastapi import APIRouter

from infrastructure.logging import logger
from infrastructure.monitoring.simple_metrics import metrics

router = APIRouter()


@router.get("/")
def get_metrics():
    logger.info("QLIQ AI Assistant Metrics")
    return metrics.get_metrics()
