from fastapi import APIRouter

from interface.schemas.recommendation_schema import RecommendationResponse

router = APIRouter()


@router.get("/{user_id}")
def get_recommendations(user_id: str) -> RecommendationResponse:
    # Placeholder recommendations
    return RecommendationResponse(
        user_id=user_id,
        recommended_products=["prod_001", "prod_002"],
        recommended_gigs=["gig_001", "gig_002"]
    )
