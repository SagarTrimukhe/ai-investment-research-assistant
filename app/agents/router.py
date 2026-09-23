from app.core.state import AgentState


def router_node(state: AgentState) -> AgentState:
    """Validates and normalizes input before sending to the research agents."""
    # TODO: add support for multiple tickers at once
    raw_ticker = state.get("ticker") or "AAPL"
    ticker = str(raw_ticker).strip().upper()
    raw_benchmark = state.get("benchmark")
    benchmark = str(raw_benchmark).strip().upper() if raw_benchmark else ""

    if not benchmark or benchmark == ticker:
        benchmark = "MSFT" if ticker != "MSFT" else "GOOGL"

    return {
        "ticker": ticker,
        "benchmark": benchmark,
    }
