from typing import List, Dict, Any, Optional  # noqa
from pydantic import BaseModel, Field
from app.core.state import AgentState
from app.core.llm import get_llm
from app.tools.financial_tools import (
    get_stock_price_volatility,
    search_sec_filings,
)


class InvestmentMemoOutput(BaseModel):
    rating: str = Field(description="Investment rating: 'BUY', 'HOLD', or 'SELL'")
    target_price: float = Field(description="12-month target price estimate in USD")
    upside_potential_pct: float = Field(description="Estimated percentage upside/downside to target price")
    executive_summary: str = Field(description="2-3 sentence executive investment summary")
    thesis_points: List[str] = Field(description="3-4 core investment pillars supporting the rating")
    key_risks: List[str] = Field(description="Key business, valuation, or macro risk factors")
    catalysts: List[str] = Field(description="Upcoming catalysts (e.g. product releases, earnings, margin expansion)")


def summary_agent_node(state: AgentState) -> dict:
    """Combines all the previous agent results and generates a final investment memo."""
    
    ticker = state.get("ticker", "AAPL").upper()
    benchmark = state.get("benchmark", "MSFT").upper()

    fundamentals = state.get("fundamentals", {})
    sentiment = state.get("sentiment", {})
    comparison = state.get("comparison", {})
    existing_risks = state.get("risks", [])

    fund_metrics = fundamentals.get("metrics", {})
    fund_summary = fundamentals.get("summary", "No filing fundamentals available.")
    sent_label = sentiment.get("label", "Neutral")
    sent_summary = sentiment.get("summary", "No news sentiment available.")
    comp_verdict = comparison.get("verdict", "No comparative verdict available.")
    rel_valuation = comparison.get("relative_valuation_summary", "")

    tools = [get_stock_price_volatility, search_sec_filings]
    tool_map = {t.name: t for t in tools}
    tools_called: List[str] = []
    volatility_data: Dict[str, Any] = {}

    llm = get_llm(temperature=0.2)

    try:
        llm_with_tools = llm.bind_tools(tools)
        tool_prompt = (
            f"You are drafting an investment memo for {ticker}. "
            f"Use the volatility tool to check {ticker}'s annualized volatility and drawdown risk."
        )
        ai_msg = llm_with_tools.invoke(tool_prompt)
        if ai_msg.tool_calls:
            for call in ai_msg.tool_calls:
                fn_name = call.get("name")
                args = call.get("args", {})
                if fn_name in tool_map:
                    res = tool_map[fn_name].invoke(args)
                    tools_called.append(fn_name)
                    if fn_name == "get_stock_price_volatility":
                        volatility_data = res
    except Exception:
        pass

    if not volatility_data or "error" in volatility_data:
        volatility_data = get_stock_price_volatility.invoke({"ticker": ticker, "period": "6mo"})
        if not tools_called:
            tools_called.append("get_stock_price_volatility")

    ann_vol = volatility_data.get("annualized_volatility_pct", "N/A")
    max_dd = volatility_data.get("max_drawdown_pct", "N/A")
    latest_price = volatility_data.get("latest_close") or 150.0

    structured_llm = llm.with_structured_output(InvestmentMemoOutput)

    prompt = f"""Analyze the financial research data for {ticker} (current price: ${latest_price}) compared to benchmark {benchmark}.

Research Findings:
- Financials (from 10-K): {fund_metrics}
- Summary: {fund_summary}
- Identified Risks: {existing_risks}
- Market Sentiment: {sent_label} ({sent_summary})
- Valuation Comparison: {rel_valuation}
- Comparative Summary: {comp_verdict}
- 6-Month Volatility: {ann_vol}%, Max Drawdown: {max_dd}%

Based on these findings, provide an investment summary including:
1. An investment rating: 'BUY', 'HOLD', or 'SELL'
2. A 12-month target price estimate based on the current price of ${latest_price}
3. Estimated percentage upside or downside
4. A brief executive summary (2-3 sentences)
5. 3-4 core thesis points
6. Main risk factors
7. Upcoming catalysts
"""

    try:
        data: InvestmentMemoOutput = structured_llm.invoke(prompt)
        
        # handle case where target price might have string symbols or formatting
        try:
            target_price_val = float(str(data.target_price).replace("$", "").replace(",", "").strip())
        except (ValueError, TypeError):
            target_price_val = float(latest_price)

        thesis = {
            "executive_summary": data.executive_summary,
            "rating": data.rating.upper(),
            "target_price": target_price_val,
            "upside_potential_pct": data.upside_potential_pct,
            "current_price": latest_price,
            "thesis_points": data.thesis_points,
            "key_risks": data.key_risks,
            "catalysts": data.catalysts,
            "volatility_metrics": volatility_data,
            "tools_used": tools_called,
        }
        return {
            "rating": data.rating.upper(),
            "target_price": target_price_val,
            "draft_thesis": thesis,
            "risks": data.key_risks,
        }
    except Exception as e:
        print("summary agent failed, using fallback:", e)
        fallback_risks = existing_risks or [f"Competition from {benchmark}.", "Market volatility and macroeconomic factors."]
        thesis = {
            "executive_summary": f"Research synthesis for {ticker} based on available metrics and comparison with {benchmark}.",
            "rating": "HOLD",
            "target_price": float(latest_price),
            "upside_potential_pct": 0.0,
            "current_price": latest_price,
            "thesis_points": [
                f"Core business position in key operating markets.",
                f"Comparative valuation relative to peer {benchmark}.",
                f"Current market sentiment is {sent_label.lower()}.",
            ],
            "key_risks": fallback_risks,
            "catalysts": ["Upcoming quarterly earnings release."],
            "volatility_metrics": volatility_data,
            "tools_used": tools_called,
        }
        return {
            "rating": "HOLD",
            "target_price": float(latest_price),
            "draft_thesis": thesis,
            "risks": fallback_risks,
        }
