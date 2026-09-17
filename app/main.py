import os
import sys

# ensure project root is on python path regardless of how streamlit is launched
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.agents.market_research import market_research_node
from app.agents.trend_analysis import trend_analysis_node

st.set_page_config(
    page_title="AI Investment Research Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("AI Investment Research Assistant")
st.caption("Theme 15 — Multi-Agent Research with Human-in-the-Loop Review")

tab_ingest, tab_analysis, tab_review = st.tabs([
    "Document Ingestion",
    "Research & Analysis",
    "Analyst Review (HITL)",
])

with tab_ingest:
    st.subheader("Upload Filings & Reports")
    uploaded_files = st.file_uploader(
        "Upload 10-K, 10-Q, or market research PDFs",
        type=["pdf"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} document(s)")
        if st.button("Process & Index to Vector DB"):
            st.info("Ingestion pipeline queued.")

with tab_analysis:
    st.subheader("Run Multi-Agent Analysis")
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Target Ticker", value="AAPL")
    with col2:
        benchmark = st.text_input("Benchmark Ticker", value="MSFT")

    if st.button("Start Research Workflow"):
        # step 1: market research (10-K RAG)
        with st.spinner(f"Running market research agent for {ticker}..."):
            state = {"ticker": ticker}
            state = market_research_node(state)

        # step 2: trend and sentiment analysis
        with st.spinner(f"Analyzing market trends and sentiment for {ticker}..."):
            state = trend_analysis_node(state)

        st.success(f"Analysis completed for {ticker}")

        # display fundamental metrics
        fundamentals = state.get("fundamentals", {})
        metrics = fundamentals.get("metrics", {})
        summary = fundamentals.get("summary", "")
        risks = state.get("risks", [])

        if metrics:
            st.subheader("Key Financial Metrics")
            m_cols = st.columns(len(metrics))
            for col, (k, v) in zip(m_cols, metrics.items()):
                label = k.replace("_", " ").title()
                col.metric(label, v)

        if summary:
            st.subheader("Performance Summary")
            st.write(summary)

        # display market sentiment & sector trends
        sentiment = state.get("sentiment", {})
        if sentiment:
            st.subheader("Market Sentiment & Sector Trends")
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.metric("Sentiment Label", sentiment.get("label", "Neutral"))
            with s_col2:
                st.metric("Sentiment Score", f"{sentiment.get('score', 0.0):+.2f}")

            if sentiment.get("summary"):
                st.write(sentiment.get("summary"))

            tailwinds = sentiment.get("sector_tailwinds", [])
            if tailwinds:
                st.markdown("**Sector Catalysts & Tailwinds:**")
                for item in tailwinds:
                    st.markdown(f"- {item}")

            macro_risks = sentiment.get("macro_risks", [])
            if macro_risks:
                st.markdown("**Macro & Regulatory Headwinds:**")
                for item in macro_risks:
                    st.markdown(f"- {item}")

        # display filing risk factors
        if risks:
            st.subheader("SEC Filing Risks")
            for r in risks:
                st.markdown(f"- {r}")

with tab_review:
    st.subheader("Human-in-the-Loop Review")
    st.info("No reports currently waiting for review.")
