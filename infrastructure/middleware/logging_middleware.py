# infrastructure/middleware/logging_middleware.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from infrastructure.logging import logger
from infrastructure.monitoring.simple_metrics import metrics

class SimpleLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate process time
        process_time = time.time() - start_time
        
        # Log response time
        logger.info(f"Response: {response.status_code} - Took {process_time:.2f}s")
        
        # Record metrics
        metrics.record_request(
            endpoint=request.url.path,
            status_code=response.status_code,
            response_time=process_time
        )
        
        return response