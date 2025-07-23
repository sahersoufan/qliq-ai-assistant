from fastapi import APIRouter, HTTPException
from interface.schemas.onboarding_schema import OnboardingRequest, OnboardingResponse

router = APIRouter()

@router.post("/")
def onboard_user(data: OnboardingRequest) -> OnboardingResponse:
    # Placeholder logic
    summary = f"Welcome, {data.name}! You're an aspiring {data.user_type}."
    return OnboardingResponse(summary=summary)
