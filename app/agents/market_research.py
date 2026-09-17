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


def market_research_node(state: AgentState) -> dict:
    """Pulls SEC filing chunks from chroma and extracts financial data."""
    ticker = state.get("ticker", "AAPL")

    # pull relevant chunks from chroma
    store = get_vector_store()
    query = f"{ticker} financial results revenue operating income risk factors"
    docs = []
    try:
        docs = store.similarity_search(query, k=4, filter={"ticker": ticker})
    except Exception:
        docs = []

    if not docs:
        all_docs = store.similarity_search(query, k=4)
        if ticker == "AAPL":
            docs = all_docs
        else:
            docs = [d for d in all_docs if d.metadata.get("ticker") == ticker]

    if not docs:
        return {
            "fundamentals": {
                "metrics": {},
                "summary": f"No SEC filing data found for {ticker} in vector database. Please upload a 10-K filing to extract fundamentals.",
            },
            "risks": [f"No 10-K filing available in ChromaDB for {ticker}."],
        }

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
        return {
            "fundamentals": {
                "metrics": data.fundamentals.model_dump(),
                "summary": data.summary,
            },
            "risks": data.risks,
        }
    except Exception as e:
        print("structured extraction failed:", e)
        return {
            "fundamentals": {"raw_notes": "Extraction failed"},
            "risks": [],
        }
