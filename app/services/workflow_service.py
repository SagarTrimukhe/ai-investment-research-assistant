from langgraph.graph import StateGraph, START, END
from app.core.state import AgentState
from app.agents.market_research import market_research_node
from app.agents.trend_analysis import trend_analysis_node


class WorkflowService:
    """Orchestrates the multi-agent equity research workflow using LangGraph.

    Graph Topology:
        START -> market_research (Node 1) -> trend_analysis (Node 2) -> END
    """

    def __init__(self):
        self.graph = self.build_graph()

    def build_graph(self):
        builder = StateGraph(AgentState)

        # ── 1. Define Nodes ──
        # Nodes are individual agent functions that receive the shared state,
        # perform specialized work (RAG, LLM reasoning), and return state updates.
        builder.add_node("market_research", market_research_node)
        builder.add_node("trend_analysis", trend_analysis_node)

        # ── 2. Define Edges ──
        # Edges define the control flow and order in which nodes execute:
        # Edge 1: START connects to market_research (entry point)
        # Edge 2: market_research connects to trend_analysis (sequential transition)
        # Edge 3: trend_analysis connects to END (completion)
        builder.add_edge(START, "market_research")
        builder.add_edge("market_research", "trend_analysis")
        builder.add_edge("trend_analysis", END)

        return builder.compile()

    def run(self, initial_state: dict) -> AgentState:
        """Execute the LangGraph workflow from START through all edges to END."""
        return self.graph.invoke(initial_state)

    def stream(self, initial_state: dict):
        """Stream state updates node-by-node as execution flows through the edges."""
        return self.graph.stream(initial_state)
