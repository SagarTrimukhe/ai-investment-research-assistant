from typing import List, Literal
import json
from pydantic import BaseModel, Field
from app.core.state import AgentState
from app.core.llm import get_llm


class TrendAnalysisOutput(BaseModel):
    sentiment_label: Literal["Bullish", "Neutral", "Bearish"] = Field(description="Bullish, Neutral, or Bearish")
    sentiment_score: float = Field(description="Score from -1.0 to 1.0")
    sector_tailwinds: List[str] = Field(description="Key sector catalysts and growth drivers")
    macro_risks: List[str] = Field(description="Macro or regulatory headwinds")
    summary: str = Field(description="Brief 1-2 sentence market trend summary")


def trend_analysis_node(state: AgentState) -> dict:
    """Looks at market sentiment and sector trends for the given ticker."""
    ticker = state.get("ticker", "AAPL")

    # grab fundamental summary from previous agent if available
    # (in parallel mode, fundamentals may not be populated yet — that's fine)
    fundamentals = state.get("fundamentals", {})
    context = fundamentals.get("summary", "") if fundamentals else ""

    llm = get_llm(temperature=0.2)
    structured_llm = llm.with_structured_output(TrendAnalysisOutput)

    prompt = f"""You are an equity analyst assessing industry trends and sentiment for {ticker}.
Company backdrop:
{context}

Analyze current market sentiment, macroeconomic conditions, and key sector tailwinds for {ticker}.
"""

    try:
        data: TrendAnalysisOutput = structured_llm.invoke(prompt)
        return {
            "sentiment": {
                "label": data.sentiment_label,
                "score": data.sentiment_score,
                "sector_tailwinds": data.sector_tailwinds,
                "macro_risks": data.macro_risks,
                "summary": data.summary,
            },
        }
    except Exception as e:
        print("trend analysis failed:", e)
        return {
            "sentiment": {
                "label": "Neutral",
                "score": 0.0,
                "summary": "Failed to extract sentiment data",
            },
        }
