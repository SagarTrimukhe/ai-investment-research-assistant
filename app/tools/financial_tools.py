import numpy as np
from langchain_core.tools import tool
from app.integrations.market_data import (
    fetch_valuation_metrics,
    fetch_stock_overview,
    fetch_price_history,
)
from app.integrations.vector_store import get_vector_store


@tool
def get_stock_valuation_metrics(ticker: str) -> dict:
    """Fetch valuation multiples (P/E, forward P/E, PEG, P/B, EV/EBITDA, profit margin) for a stock ticker."""
    metrics = fetch_valuation_metrics(ticker)
    if not metrics:
        return {"error": f"Unable to fetch valuation metrics for {ticker}"}
    return metrics


@tool
def get_stock_overview(ticker: str) -> dict:
    """Fetch basic stock profile including current price, market cap, 52-week range, and sector/industry."""
    overview = fetch_stock_overview(ticker)
    if not overview:
        return {"error": f"Unable to fetch overview for {ticker}"}
    return overview


@tool
def get_stock_price_volatility(ticker: str, period: str = "6mo") -> dict:
    """Fetch historical daily price action and calculate realized annualized volatility and max drawdown."""
    try:
        hist = fetch_price_history(ticker, period=period)
        if hist.empty or len(hist) < 5:
            return {"error": f"Insufficient price history for {ticker}"}

        close = hist["Close"]
        returns = close.pct_change().dropna()
        # Annualized volatility (252 trading days)
        ann_vol = float(returns.std() * np.sqrt(252)) * 100
        # Total period return
        period_return = float((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100
        # Max drawdown
        rolling_max = close.cummax()
        drawdown = (close - rolling_max) / rolling_max
        max_drawdown = float(drawdown.min()) * 100

        return {
            "ticker": ticker.upper(),
            "period": period,
            "annualized_volatility_pct": round(ann_vol, 2),
            "period_return_pct": round(period_return, 2),
            "max_drawdown_pct": round(max_drawdown, 2),
            "latest_close": round(float(close.iloc[-1]), 2),
        }
    except Exception as e:
        return {"error": f"Failed to compute volatility for {ticker}: {e}"}


@tool
def search_sec_filings(ticker: str, query: str) -> str:
    """Search vector database of SEC 10-K filings for disclosures, risk factors, or financial notes."""
    try:
        store = get_vector_store()
        docs = []
        try:
            docs = store.similarity_search(query, k=3, filter={"ticker": ticker.upper()})
        except Exception:
            docs = []

        if not docs:
            docs = store.similarity_search(f"{ticker} {query}", k=3)

        if not docs:
            return f"No SEC 10-K filing chunks found for {ticker} matching '{query}'."

        snippets = [f"[Filing Excerpt {i+1}]: {doc.page_content.strip()}" for i, doc in enumerate(docs)]
        return "\n\n".join(snippets)
    except Exception as e:
        return f"Error querying vector store: {e}"


# List of all available financial tools for autonomous agent binding
FINANCIAL_TOOLS = [
    get_stock_valuation_metrics,
    get_stock_overview,
    get_stock_price_volatility,
    search_sec_filings,
]
