# AI Investment Research Assistant (Theme 15)

Multi-agent equity research system built with LangGraph, ChromaDB, and Streamlit, featuring parallel analysis workflows and a Human-in-the-Loop (HITL) analyst approval checkpoint.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY / GEMINI_API_KEY and AWS credentials
   ```

## Running the Application

```bash
streamlit run app/main.py
```

## Architecture

- **Ingestion & Storage**: PyPDF / pdfplumber parses filings and reports into ChromaDB; raw files sync to S3.
- **Multi-Agent Runtime (LangGraph)**:
  - `router_node`: Dispatches queries to parallel branches.
  - `market_research_node`: Pulls fundamentals and 10-K disclosures (retriever + yfinance).
  - `trend_analysis_node`: Evaluates macro climate, sector rotation, and news sentiment.
  - `comparative_analysis_node`: Joins branches and computes valuation multiples.
  - `summary_agent_node`: Compiles draft investment memorandum.
  - `human_approval_gate_node`: Freezes state with LangGraph `interrupt()` for analyst sign-off before export.
- **Frontend**: Streamlit dashboard (Ingestion, Analysis, Review).
# ai-investment-research-assistant