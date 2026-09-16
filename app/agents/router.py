from app.core.state import AgentState


def router_node(state: AgentState) -> AgentState:
    """Validates and normalizes input before sending to the research agents."""
    ticker = state.get("ticker", "AAPL").upper()
    benchmark = state.get("benchmark")

    if benchmark.upper() == ticker:
        benchmark = "MSFT" if ticker != "MSFT" else "GOOGL"

    return {
        "ticker": ticker,
        "benchmark": benchmark.upper(),
    }
