import json
import re
from app.core.state import AgentState
from app.integrations.vector_store import get_vector_store
from app.core.llm import get_llm


def market_research_node(state: AgentState) -> AgentState:
    ticker = state.get("ticker", "AAPL")
    
    # pull relevant chunks from chroma
    store = get_vector_store()
    query = f"{ticker} financial results revenue operating income risk factors"
    docs = store.similarity_search(query, k=4)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # prompt gemini to pull out the key numbers
    llm = get_llm(temperature=0.1)
    prompt = f"""You are a financial analyst researching {ticker}.
Based on the following excerpts from company SEC filings, extract key financial numbers and risks.

Context:
{context}

Respond ONLY with a JSON object in this exact format:
{{
  "fundamentals": {{
    "total_revenue": "...",
    "operating_income": "...",
    "products_revenue": "...",
    "services_revenue": "..."
  }},
  "summary": "Brief 1-2 sentence performance summary",
  "risks": [
    "first key risk",
    "second key risk"
  ]
}}
"""
    response = llm.invoke(prompt)
    
    # try parsing the json response
    try:
        clean_text = re.sub(r"```json\s*|\s*```", "", response.content).strip()
        data = json.loads(clean_text)
        state["fundamentals"] = {
            "metrics": data.get("fundamentals", {}),
            "summary": data.get("summary", "")
        }
        state["risks"] = data.get("risks", [])
    except Exception as e:
        print(f"warning: could not parse LLM response: {e}")
        state["fundamentals"] = {"raw_notes": response.content}
        state["risks"] = []

    return state
