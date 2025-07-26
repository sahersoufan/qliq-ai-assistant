# infrastructure/logging.py
import sys
from loguru import logger

# Remove default handler and add customized ones
logger.remove()
# Console output
logger.add(sys.stdout, level="INFO")
# File output with rotation
logger.add("logs/app.log", rotation="1 MB", level="INFO")

# Simple context logger
def get_logger(context=None):
    if context:
        return logger.bind(**context)
    return logger
