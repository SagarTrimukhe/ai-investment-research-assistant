from pydantic import BaseModel
from typing import Optional


class ReviewDecision(BaseModel):
    approved: bool
    rating_override: Optional[str] = None
    target_price_override: Optional[float] = None
    feedback: Optional[str] = None
