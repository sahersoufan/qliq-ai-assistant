from typing import Literal, List

from pydantic import BaseModel


class ComparisonResult(BaseModel):
    query: str
    ml_label: Literal["FAQ", "Product", "Gig", "General"]
    rule_based_label: Literal["FAQ", "Product", "Gig", "General"]
    match: bool


class ComparisonResponse(BaseModel):
    results: List[ComparisonResult]
    match_rate: float
