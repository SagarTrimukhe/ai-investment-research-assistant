from pydantic import BaseModel
from typing import List, Optional


class ResearchReport(BaseModel):
    ticker: str
    recommendation: str
    target_price: Optional[float] = None
    thesis_points: List[str] = []
    risks: List[str] = []
    analyst_approved: bool = False
