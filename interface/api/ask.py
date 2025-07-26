# interface/api/ask.py
import traceback

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from domain.services.query_service import QueryService
from infrastructure.ml.sklearn_query_classifier_service import SklearnQueryClassifierService
from interface.schemas.query_schema import QueryRequest, QueryResponse
from infrastructure.logging import logger

router = APIRouter()
query_service = QueryService(classifier=SklearnQueryClassifierService())


@router.post("/", response_model=QueryResponse)
def ask_question(request: Request, data: QueryRequest):
    try:
        # Log the incoming request
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"Received query request from {client_ip}")
        
        # Validate input
        if not data.query or not data.query.strip():
            logger.warning(f"Empty query received from {client_ip}")
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        # Process the query
        logger.info(f"Processing query: {data.query[:50]}{'...' if len(data.query) > 50 else ''}")
        answer = query_service.ask(data.query)
        
        # Log success and return response
        logger.info("Query processed successfully")
        return QueryResponse(answer=answer)
        
    except ValidationError as e:
        # Handle validation errors from the request schema
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid request format")
        
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
        
    except Exception as e:
        # Log the full exception with traceback
        logger.error(f"Error processing query: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Return a user-friendly error message
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your request. Please try again later."
        )
