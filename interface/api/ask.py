from fastapi import APIRouter

from interface.schemas.query_schema import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/")
def ask_question(query: QueryRequest) -> QueryResponse:
    # Placeholder response
    return QueryResponse(answer="This is a mock answer to your question.")
