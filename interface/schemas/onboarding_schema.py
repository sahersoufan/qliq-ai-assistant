# Pydantic models for onboarding requests/responses
from typing import List

from pydantic import BaseModel


class OnboardingRequest(BaseModel):
    name: str
    user_type: str  # Influencer, Vendor, Buyer
    interests: List[str]
    goals: List[str]
    language: str = "en"


class OnboardingResponse(BaseModel):
    summary: str
