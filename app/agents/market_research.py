from typing import List
from pydantic import BaseModel, Field
from app.core.state import AgentState
from app.integrations.vector_store import get_vector_store
from app.core.llm import get_llm


class FinancialMetrics(BaseModel):
    total_revenue: str = Field(description="Total net sales or revenue")
    operating_income: str = Field(description="Operating income")
    products_revenue: str = Field(description="Revenue from products")
    services_revenue: str = Field(description="Revenue from services")


class MarketResearchOutput(BaseModel):
    fundamentals: FinancialMetrics
    summary: str = Field(description="Brief 1-2 sentence performance summary")
    risks: List[str] = Field(description="List of key business risks")


def market_research_node(state: AgentState) -> AgentState:
    ticker = state.get("ticker", "AAPL")

    # pull relevant chunks from chroma
    store = get_vector_store()
    query = f"{ticker} financial results revenue operating income risk factors"
    docs = store.similarity_search(query, k=4)

    if not docs:
        state["fundamentals"] = {"summary": f"No filing data found for {ticker}."}
        state["risks"] = []
        return state

    context = "\n\n".join([doc.page_content for doc in docs])

    # prompt gemini with pydantic structured output
    llm = get_llm(temperature=0.1)
    structured_llm = llm.with_structured_output(MarketResearchOutput)

    prompt = f"""You are a financial analyst researching {ticker}.
Based on the following excerpts from company SEC filings, extract key financial numbers and risks.

Context:
{context}
"""

    try:
        data: MarketResearchOutput = structured_llm.invoke(prompt)
        state["fundamentals"] = {
            "metrics": data.fundamentals.model_dump(),
            "summary": data.summary,
        }
        state["risks"] = data.risks
    except Exception as e:
        print(f"warning: structured output extraction failed: {e}")
        state["fundamentals"] = {"raw_notes": "Extraction failed"}
        state["risks"] = []

    return state
