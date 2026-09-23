# AI Investment Research Assistant

A multi-agent equity research assistant built with LangGraph, ChromaDB, and Streamlit, featuring automated financial report analysis, peer benchmarking, and a Human-in-the-Loop (HITL) analyst review gate.

## Key Features

- **Document Ingestion**: Extracts and chunks SEC 10-K and 10-Q reports into ChromaDB vector storage.
- **Fundamental Research (RAG)**: Retrieves filing chunks to extract revenue, income, and business risks.
- **Trend & Sentiment Analysis**: Gauges market sentiment, macro factors, and industry catalysts.
- **Comparative Peer Analysis**: Pulls live valuation multiples (P/E, Forward P/E, Market Cap) via yfinance.
- **Investment Thesis Synthesis**: Generates draft investment recommendations, price targets, and catalyst summaries.
- **Human-in-the-Loop Review**: Interrupts the workflow before final output to allow analysts to review, adjust, or certify findings.

## Setup & Installation

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
   # Add your GEMINI_API_KEY
   ```

## Running the Application

```bash
streamlit run app/main.py
```
