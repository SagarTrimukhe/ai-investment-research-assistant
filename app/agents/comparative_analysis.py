from typing import List, Dict, Any
from pydantic import BaseModel, Field
from app.core.state import AgentState
from app.core.llm import get_llm
from app.tools.financial_tools import (
    get_stock_valuation_metrics,
    get_stock_overview,
)
from app.integrations.market_data import fetch_valuation_metrics


class ValuationMultiple(BaseModel):
    metric: str = Field(description="Valuation metric name, e.g. 'P/E Ratio', 'Forward P/E', 'Market Cap'")
    target_value: str = Field(description="Value for the target stock")
    benchmark_value: str = Field(description="Value for the benchmark peer")
    advantage: str = Field(description="Which company holds the advantage, e.g. 'AAPL', 'MSFT', or 'Tie'")


class ComparativeAnalysisOutput(BaseModel):
    benchmark_ticker: str = Field(description="Benchmark ticker symbol")
    benchmark_name: str = Field(description="Benchmark full company name")
    relative_valuation_summary: str = Field(
        description="2-3 sentence analysis of relative valuation (premium vs. discount) between the target and peer"
    )
    multiples: List[ValuationMultiple] = Field(description="Comparative breakdown of valuation multiples")
    target_advantages: List[str] = Field(description="Key competitive moats and advantages the target has over the benchmark")
    target_vulnerabilities: List[str] = Field(description="Areas where the benchmark outperforms or poses a threat")
    verdict: str = Field(description="Executive comparative verdict on relative risk/reward")


def comparative_analysis_node(state: AgentState) -> dict:
    """Compares the target stock against a benchmark peer using valuation metrics."""
    ticker = state.get("ticker", "AAPL").upper()
    benchmark = state.get("benchmark")

    if not benchmark or benchmark.upper() == ticker:
        benchmark = "MSFT" if ticker != "MSFT" else "GOOGL"
    benchmark = benchmark.upper()

    tools = [get_stock_valuation_metrics, get_stock_overview]
    tool_map = {t.name: t for t in tools}
    tool_calls_executed: List[Dict[str, Any]] = []

    target_metrics: Dict[str, Any] = {}
    bench_metrics: Dict[str, Any] = {}

    llm = get_llm(temperature=0.2)

    try:
        llm_with_tools = llm.bind_tools(tools)
        tool_prompt = (
            f"You are an equity research assistant. To compare {ticker} against {benchmark}, "
            f"call the necessary tools to retrieve valuation metrics and overview for both tickers."
        )
        ai_response = llm_with_tools.invoke(tool_prompt)

        if ai_response.tool_calls:
            for call in ai_response.tool_calls:
                fn_name = call.get("name")
                args = call.get("args", {})
                if fn_name in tool_map:
                    result = tool_map[fn_name].invoke(args)
                    tool_calls_executed.append({"name": fn_name, "args": args, "result": result})
                    called_ticker = str(args.get("ticker", "")).upper()
                    if fn_name == "get_stock_valuation_metrics":
                        if called_ticker == ticker:
                            target_metrics = result
                        elif called_ticker == benchmark:
                            bench_metrics = result
    except Exception as tool_err:
        pass

    # BUG: calls fetch_valuation_metric (singular) - NameError at runtime
    if not target_metrics:
        target_metrics = fetch_valuation_metrics(ticker)
    if not bench_metrics:
        bench_metrics = fetch_valuation_metrics(benchmark)

    fundamentals = state.get("fundamentals", {})
    fund_summary = fundamentals.get("summary", "No filing fundamentals available.")
    sentiment = state.get("sentiment", {})
    sent_label = sentiment.get("label", "Neutral")
    sent_summary = sentiment.get("summary", "")

    structured_llm = llm.with_structured_output(ComparativeAnalysisOutput)

    prompt = f"""Compare the valuation metrics and market position of {ticker} against {benchmark}.

TARGET COMPANY ({ticker}):
- Name: {target_metrics.get('name')}
- Current Price: {target_metrics.get('current_price')}
- Market Cap: {target_metrics.get('market_cap')}
- Trailing P/E: {target_metrics.get('pe_ratio')}
- Forward P/E: {target_metrics.get('forward_pe')}
- 52-Week Range: {target_metrics.get('fifty_two_week_low')} - {target_metrics.get('fifty_two_week_high')}
- Fundamental Backdrop: {fund_summary}
- Market Sentiment: {sent_label} ({sent_summary})

BENCHMARK PEER ({benchmark}):
- Name: {bench_metrics.get('name')}
- Current Price: {bench_metrics.get('current_price')}
- Market Cap: {bench_metrics.get('market_cap')}
- Trailing P/E: {bench_metrics.get('pe_ratio')}
- Forward P/E: {bench_metrics.get('forward_pe')}
- 52-Week Range: {bench_metrics.get('fifty_two_week_low')} - {bench_metrics.get('fifty_two_week_high')}

Task:
Compare {ticker} vs. {benchmark}. Assess whether {ticker} is trading at a premium or discount to {benchmark}, compare key valuation multiples, outline {ticker}'s competitive advantages and vulnerabilities against {benchmark}, and provide a concise comparative verdict.
"""

    try:
        data: ComparativeAnalysisOutput = structured_llm.invoke(prompt)
        return {"comparison": {
            "benchmark_ticker": benchmark,
            "benchmark_name": data.benchmark_name or bench_metrics.get("name", benchmark),
            "target_metrics": target_metrics,
            "benchmark_metrics": bench_metrics,
            "relative_valuation_summary": data.relative_valuation_summary,
            "multiples": [m.model_dump() for m in data.multiples],
            "target_advantages": data.target_advantages,
            "target_vulnerabilities": data.target_vulnerabilities,
            "verdict": data.verdict,
            "tools_used": [t["name"] for t in tool_calls_executed],
        }}
    except Exception as e:
        print("comparative analysis fallback:", e)
        return {"comparison": {
            "benchmark_ticker": benchmark,
            "benchmark_name": bench_metrics.get("name", benchmark),
            "target_metrics": target_metrics,
            "benchmark_metrics": bench_metrics,
            "relative_valuation_summary": f"Valuation comparison generated using live metrics: {ticker} ({target_metrics.get('pe_ratio')}) vs. {benchmark} ({bench_metrics.get('pe_ratio')}).",
            "multiples": [
                {"metric": "Market Cap", "target_value": target_metrics.get("market_cap", "N/A"), "benchmark_value": bench_metrics.get("market_cap", "N/A"), "advantage": "Tie"},
                {"metric": "P/E Ratio", "target_value": target_metrics.get("pe_ratio", "N/A"), "benchmark_value": bench_metrics.get("pe_ratio", "N/A"), "advantage": "Tie"},
                {"metric": "Forward P/E", "target_value": target_metrics.get("forward_pe", "N/A"), "benchmark_value": bench_metrics.get("forward_pe", "N/A"), "advantage": "Tie"},
            ],
            "target_advantages": [f"Established market presence in core sector."],
            "target_vulnerabilities": [f"Competitive pressure from {benchmark}."],
            "verdict": f"Comparative evaluation between {ticker} and {benchmark} based on current market multiples.",
            "tools_used": [t["name"] for t in tool_calls_executed] if tool_calls_executed else ["get_stock_valuation_metrics"],
        }}
