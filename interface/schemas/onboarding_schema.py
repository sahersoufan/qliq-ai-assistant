# Pydantic models for onboarding requests/responses
from typing import List

from pydantic import BaseModel


class OnboardingRequest(BaseModel):
    message: str


class OnboardingResponse(BaseModel):
    response: str
