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

        # add all the agent nodes
        builder.add_node("router", router_node)
        builder.add_node("market_research", market_research_node)
        builder.add_node("trend_analysis", trend_analysis_node)
        builder.add_node("comparative_analysis", comparative_analysis_node)
        builder.add_node("summary_agent", summary_agent_node)
        builder.add_node("human_approval_gate", human_approval_gate_node)

        # connect the nodes together
        builder.add_edge(START, "router")

        # router sends to both research agents in parallel
        builder.add_edge("router", "market_research")
        builder.add_edge("router", "trend_analysis")

        # both feed into comparative analysis
        builder.add_edge("market_research", "comparative_analysis")
        builder.add_edge("trend_analysis", "comparative_analysis")

        builder.add_edge("comparative_analysis", "summary_agent")

        # summary goes to human review before finishing
        builder.add_edge("summary_agent", "human_approval_gate")

        builder.add_edge("human_approval_gate", END)

        # need checkpointer for the interrupt/resume to work
        return builder.compile(checkpointer=self.checkpointer)

    def run(self, initial_state: dict, thread_id: str = "default") -> dict:
        """Run the full workflow."""
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke(initial_state, config)

    def stream(self, initial_state: dict, thread_id: str = "default"):
        """Stream results node by node."""
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.stream(initial_state, config)

    def resume(self, decision: dict, thread_id: str = "default"):
        """Resume after the human review step."""
        from langgraph.types import Command
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.invoke(Command(resume=decision), config)

    def get_state(self, thread_id: str = "default"):
        """Check current graph state."""
        config = {"configurable": {"thread_id": thread_id}}
        return self.graph.get_state(config)
