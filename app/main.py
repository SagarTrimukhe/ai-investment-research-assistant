import streamlit as st

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
        st.write(f"Initiating research for {ticker} vs {benchmark}...")

with tab_review:
    st.subheader("Human-in-the-Loop Review")
    st.info("No reports currently waiting for review.")
