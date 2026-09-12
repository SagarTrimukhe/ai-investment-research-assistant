from langgraph.types import interrupt
from app.core.state import AgentState


def human_approval_gate_node(state: AgentState) -> AgentState:
    # Freezes graph execution awaiting senior analyst review
    decision = interrupt({
        "ticker": state.get("ticker"),
        "draft_thesis": state.get("draft_thesis"),
        "rating": state.get("rating"),
        "target_price": state.get("target_price"),
    })

    if isinstance(decision, dict):
        state["approved"] = decision.get("approved", False)
        state["feedback"] = decision.get("feedback")

    return state
