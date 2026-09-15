from typing import TypedDict, Optional, List, Dict, Any, Annotated


def _keep_latest(current, new):
    """Reducer for parallel fan-in: keep the latest non-None value."""
    return new if new is not None else current


class AgentState(TypedDict, total=False):
    ticker: Annotated[str, _keep_latest]
    benchmark: Annotated[Optional[str], _keep_latest]
    fundamentals: Annotated[Dict[str, Any], _keep_latest]
    sentiment: Annotated[Dict[str, Any], _keep_latest]
    comparison: Annotated[Dict[str, Any], _keep_latest]
    draft_thesis: Annotated[Dict[str, Any], _keep_latest]
    rating: Annotated[Optional[str], _keep_latest]
    target_price: Annotated[Optional[float], _keep_latest]
    risks: Annotated[List[str], _keep_latest]
    approved: Annotated[bool, _keep_latest]
    feedback: Annotated[Optional[str], _keep_latest]
    report_path: Annotated[Optional[str], _keep_latest]
