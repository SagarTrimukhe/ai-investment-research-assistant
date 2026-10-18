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

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if it is not already installed.

2. Sync the project dependencies:
   ```bash
   uv sync
   ```
   This creates the project virtual environment and installs the dependencies from `uv.lock`. The project requires Python 3.14; uv can install the required Python version if needed.

3. Configure environment variables by creating a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key
   ```
   Add any other service credentials you use, such as `OPENAI_API_KEY` or AWS credentials.

## Running the Application

Start the Streamlit application from the project root:

```bash
uv run streamlit run app/main.py
```
