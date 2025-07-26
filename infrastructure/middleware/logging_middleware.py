# infrastructure/middleware/logging_middleware.py
import time
import traceback
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from infrastructure.logging import logger
from infrastructure.monitoring.simple_metrics import metrics

class SimpleLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Get client information
        client_ip = request.client.host if request.client else "unknown"
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path} from {client_ip}")
        
        try:
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
            
        except Exception as e:
            # Calculate process time even for errors
            process_time = time.time() - start_time
            
            # Log the error with traceback
            logger.error(f"Unhandled exception processing {request.method} {request.url.path}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Record error metrics
            metrics.record_request(
                endpoint=request.url.path,
                status_code=500,  # Internal server error
                response_time=process_time
            )
            
            # Return a JSON response with error information
            return JSONResponse(
                status_code=500,
                content={"detail": "An internal server error occurred. Please try again later."}
            )