from langgraph.graph import StateGraph, END
from app.core.state import AgentState


class WorkflowService:
    def build_graph(self):
        # Build LangGraph StateGraph with parallel branches and HITL interrupt
        builder = StateGraph(AgentState)
        return builder.compile()
