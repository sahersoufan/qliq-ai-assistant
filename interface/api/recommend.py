from fastapi import APIRouter, HTTPException
from domain.services.recommendation_service import recommend
from interface.schemas.recommendation_schema import RecommendationResponse

router = APIRouter()

@router.get("/{user_id}", response_model=RecommendationResponse)
def get_recommendations(user_id: str, top_k: int = 5):
    result = recommend(user_id, top_k=top_k)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
