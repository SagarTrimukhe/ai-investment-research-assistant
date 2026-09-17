import os
import sys

# ensure project root is on python path regardless of how streamlit is launched
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.agents.market_research import market_research_node
from app.agents.trend_analysis import trend_analysis_node
from app.integrations.market_data import fetch_stock_overview, fetch_price_history
from app.services.document_ingestion import (
    extract_text,
    ingest_document_text,
    get_indexed_tickers,
    is_ticker_indexed,
)

st.set_page_config(
    page_title="AI Investment Research Assistant",
    page_icon="📊",
    layout="wide",
)

# Sidebar with system status and indexed companies
with st.sidebar:
    st.header("⚙️ Research Control Center")
    st.markdown("**LLM:** Gemini 1.5 Flash (`temperature=0.1`)")
    st.markdown("**Vector Store:** ChromaDB (`financial_filings`)")
    st.divider()
    st.subheader("📚 Indexed Companies")
    indexed_list = get_indexed_tickers()
    if indexed_list:
        for t in indexed_list:
            st.markdown(f"- **{t}** — 10-K Indexed ✅")
    else:
        st.caption("No filings indexed.")
    st.divider()
    st.caption("Theme 15 • Multi-Agent Equity Research")

st.title("AI Investment Research Assistant")
st.caption("Theme 15 — Multi-Agent Research with Human-in-the-Loop Review")

tab_ingest, tab_analysis, tab_review = st.tabs([
    "Document Ingestion",
    "Research & Analysis",
    "Analyst Review (HITL)",
])

with tab_ingest:
    st.subheader("Upload Filings & Reports into ChromaDB")
    st.caption("Index 10-K, 10-Q, or market research files directly into the vector database.")

    ingest_col1, ingest_col2 = st.columns([1, 2])
    with ingest_col1:
        ingest_ticker = st.text_input("Associated Stock Ticker", value="AAPL", key="ingest_ticker_input").upper().strip()
    with ingest_col2:
        uploaded_files = st.file_uploader(
            f"Upload 10-K or research documents for {ingest_ticker}",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            key="general_uploader",
        )

    if uploaded_files:
        st.write(f"Selected **{len(uploaded_files)}** document(s) for **{ingest_ticker}**")
        if st.button(f"Process & Index to Vector DB ({ingest_ticker})", type="primary"):
            total_chunks = 0
            with st.spinner(f"Extracting, chunking, and embedding documents for {ingest_ticker}..."):
                for up_file in uploaded_files:
                    text = extract_text(up_file, up_file.name)
                    chunks = ingest_document_text(text, up_file.name, ingest_ticker)
                    total_chunks += chunks
            if total_chunks > 0:
                st.success(f"Successfully processed and indexed {total_chunks} chunks into ChromaDB for {ingest_ticker}!")
                st.rerun()
            else:
                st.error("Could not extract readable text from the uploaded files.")

    st.divider()
    st.subheader("📚 Currently Indexed Stocks in Knowledge Base")
    current_indexed = get_indexed_tickers()
    if current_indexed:
        cols = st.columns(len(current_indexed) if len(current_indexed) <= 4 else 4)
        for idx, t in enumerate(current_indexed):
            cols[idx % 4].info(f"**{t}** — Indexed ✅")
    else:
        st.caption("No filings currently indexed.")

with tab_analysis:
    st.subheader("Run Multi-Agent Analysis")
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Target Ticker", value="AAPL").upper().strip()
    with col2:
        benchmark = st.text_input("Benchmark Ticker", value="MSFT").upper().strip()

    # Check if stock has filings in Vector DB
    is_indexed = is_ticker_indexed(ticker)
    if is_indexed:
        st.success(f"**Knowledge Base Ready**: SEC 10-K filing documents for **{ticker}** are indexed in ChromaDB.", icon="✅")
    else:
        st.warning(
            f"⚠️ **{ticker} is not in the Knowledge Base**\n\n"
            f"The vector database currently does not have SEC 10-K filings indexed for **{ticker}**.\n"
            f"Please upload a filing below to enable fundamental RAG extraction, or proceed with public market data.",
            icon="⚠️",
        )
        with st.expander(f"📥 Upload & Index Filing for {ticker}", expanded=True):
            inline_file = st.file_uploader(
                f"Choose 10-K / 10-Q filing (.txt or .pdf) for {ticker}",
                type=["txt", "pdf"],
                key=f"inline_uploader_{ticker}",
            )
            if inline_file is not None:
                if st.button(f"⚡ Index Filing for {ticker}", type="secondary", key=f"btn_index_{ticker}"):
                    with st.spinner(f"Extracting and indexing {inline_file.name} for {ticker}..."):
                        text = extract_text(inline_file, inline_file.name)
                        chunks = ingest_document_text(text, inline_file.name, ticker)
                        if chunks > 0:
                            st.success(f"Indexed {chunks} chunks for {ticker}! Knowledge base updated.")
                            st.rerun()
                        else:
                            st.error("Failed to parse text from the uploaded file.")

    # interactive market price action & chart
    with st.expander(f"📈 Market Price Action — {ticker}", expanded=True):
        m_head_col, m_period_col = st.columns([3, 1])
        with m_period_col:
            period = st.selectbox(
                "Timeframe",
                options=["1mo", "3mo", "6mo", "1y", "ytd"],
                index=2,
                key="price_period",
            )

        overview = fetch_stock_overview(ticker)
        if overview and overview.get("current_price"):
            c1, c2, c3 = st.columns(3)
            c1.metric(
                label=f"{ticker} Current Price",
                value=f"${overview['current_price']:.2f}",
                delta=f"{overview['change']:+.2f} ({overview['change_pct']:+.2f}%)",
            )
            if overview.get("fifty_two_week_high"):
                c2.metric("52-Week High", f"${overview['fifty_two_week_high']:.2f}")
            if overview.get("fifty_two_week_low"):
                c3.metric("52-Week Low", f"${overview['fifty_two_week_low']:.2f}")

        history_df = fetch_price_history(ticker, period=period)
        if not history_df.empty:
            st.line_chart(history_df["Close"])
        else:
            st.caption(f"No price history found for {ticker}.")

    st.markdown("---")

    if st.button("Start Research Workflow", type="primary"):
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
            sentiment_label = sentiment.get("label", "Neutral")
            label_icon = "🟢" if sentiment_label == "Bullish" else ("🔴" if sentiment_label == "Bearish" else "🟡")
            with s_col1:
                st.metric("Sentiment Label", f"{label_icon} {sentiment_label}")
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

