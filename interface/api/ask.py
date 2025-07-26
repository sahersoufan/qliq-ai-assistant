# interface/api/ask.py
import traceback

from fastapi import APIRouter, HTTPException

from domain.services.query_service import QueryService
from infrastructure.ml.sklearn_query_classifier_service import SklearnQueryClassifierService
from interface.schemas.query_schema import QueryRequest, QueryResponse

router = APIRouter()
query_service = QueryService(classifier=SklearnQueryClassifierService())


@router.post("/", response_model=QueryResponse)
def ask_question(data: QueryRequest):
    try:
        answer = query_service.ask(data.query)
        return QueryResponse(answer=answer)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
