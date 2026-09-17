from langgraph.checkpoint import interrupt
from app.core.state import AgentState


def human_approval_gate_node(state: AgentState) -> dict:
    """Pauses the workflow so a human analyst can review before publishing."""
    decision = interrupt({
        "ticker": state.get("ticker"),
        "draft_thesis": state.get("draft_thesis"),
        "rating": state.get("rating"),
        "target_price": state.get("target_price"),
    })

    if isinstance(decision, dict):
        return {
            "approved": decision.get("approved", False),
            "feedback": decision.get("feedback"),
        }

    return {"approved": bool(decision), "feedback": None}
