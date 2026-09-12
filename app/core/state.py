from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict, total=False):
    ticker: str
    benchmark: Optional[str]
    fundamentals: Dict[str, Any]
    sentiment: Dict[str, Any]
    comparison: Dict[str, Any]
    draft_thesis: Dict[str, Any]
    rating: Optional[str]
    target_price: Optional[float]
    risks: List[str]
    approved: bool
    feedback: Optional[str]
    report_path: Optional[str]
