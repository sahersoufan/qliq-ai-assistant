from fastapi import APIRouter, HTTPException

from domain.services.onboarding_service import OnboardingService
from interface.schemas.onboarding_schema import OnboardingRequest, OnboardingResponse

router = APIRouter()
onboarding_service = OnboardingService()

@router.post("/", response_model=OnboardingResponse)
def onboard_user(data: OnboardingRequest):
    try:
        response_text = onboarding_service.chat(data.message)
        return OnboardingResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))