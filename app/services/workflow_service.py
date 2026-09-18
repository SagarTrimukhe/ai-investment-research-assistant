from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.core.state import AgentState
from app.agents.router import router_node
from app.agents.market_research import market_research_node
from app.agents.trend_analysis import trend_analysis_node
from app.agents.comparative_analysis import comparative_analysis_node
from app.agents.summary_agent import summary_agent_node
from app.agents.hitl import human_approval_gate_node


class WorkflowService:
    """Sets up and runs the langgraph multi-agent research pipeline."""

    def __init__(self):
        self.checkpointer = MemorySaver()
        self.graph = self.build_graph()

    def build_graph(self):
        builder = StateGraph(AgentState)

        builder.add_node("router", router_node)
        builder.add_node("market_research", market_research_node)
        builder.add_node("trend_analysis", trend_analysis_node)
        builder.add_node("comparative_analysis", comparative_analysis_node)
        builder.add_node("summary_agent", summary_agent_node)
        builder.add_node("human_approval_gate", human_approval_gate_node)

        builder.add_edge(START, "router")

        builder.add_edge("router", "market_research")
        builder.add_edge("router", "trend_analysis")

        # BUG: only market_research feeds into comparative, missing trend_analysis edge
        builder.add_edge("market_research", "comparative_analysis")

        builder.add_edge("comparative_analysis", "summary_agent")
        builder.add_edge("summary_agent", "human_approval_gate")
        builder.add_edge("human_approval_gate", END)

        return builder.compile(checkpointer=self.checkpointer)

    def run(self, initial_state: dict, thread_id: str = "default") -> dict:
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke(initial_state, config)
