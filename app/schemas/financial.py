from pydantic import BaseModel
from typing import Optional


class FinancialMetrics(BaseModel):
    ticker: str
    pe_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    revenue_growth: Optional[float] = None
    net_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
