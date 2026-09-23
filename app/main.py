import os
import sys
import time

# Ensure project root is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.services.workflow_service import WorkflowService
from app.integrations.market_data import fetch_stock_overview, fetch_price_history
from app.services.document_ingestion import (
    extract_text,
    ingest_document_text,
    get_indexed_tickers,
    get_indexed_summary,
    is_ticker_indexed,
    detect_ticker_from_filename,
    clear_vector_store,
)

st.set_page_config(
    page_title="AI Investment Research Assistant",
    page_icon="📊",
    layout="wide",
)

# Sidebar: System configuration and status
st.sidebar.title("Research Assistant")
st.sidebar.caption("Course Project • Multi-Agent Financial Research")

st.sidebar.subheader("System Info")
st.sidebar.text("LLM: Gemini 1.5 Flash")
st.sidebar.text("Database: ChromaDB")

indexed_list = get_indexed_tickers()
st.sidebar.subheader(f"Indexed Companies ({len(indexed_list)})")
if indexed_list:
    st.sidebar.write(", ".join(f"`{t}`" for t in indexed_list))
else:
    st.sidebar.caption("No filings indexed yet.")

st.sidebar.divider()
st.sidebar.caption("Student Project • Final Submission")


# Main title
st.title("📊 AI Investment Research Assistant")
st.caption("Automated equity research and financial report analysis using multi-agent workflows.")

tab_ingest, tab_analysis, tab_review = st.tabs([
    "Document Ingestion",
    "Research & Analysis",
    "Analyst Review (HITL)",
])


# -------------------------------------------------------------
# Tab 1: Document Ingestion
# -------------------------------------------------------------
with tab_ingest:
    st.subheader("Upload Filings & Research Reports")
    st.caption("Upload company 10-K, 10-Q, or research reports (PDF or TXT) to index into the vector database.")

    ingest_col1, ingest_col2 = st.columns([1, 2])
    with ingest_col1:
        default_ticker = st.text_input(
            "Associated Stock Ticker",
            value="AAPL",
            key="ingest_ticker_input",
            help="Stock ticker symbol for the document (e.g., AAPL, MSFT, NVDA)",
        ).upper().strip()
    with ingest_col2:
        uploaded_files = st.file_uploader(
            "Select Document Files",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            key="general_uploader",
        )

    if uploaded_files:
        st.write("##### Selected Files")
        preview_rows = []
        for up_file in uploaded_files:
            detected = detect_ticker_from_filename(up_file.name) or default_ticker
            preview_rows.append({
                "Filename": up_file.name,
                "Ticker": detected,
                "File Size (KB)": f"{len(up_file.getvalue()) / 1024:.1f}",
            })
        st.dataframe(preview_rows, use_container_width=True)

        if st.button(f"Upload and Index {len(uploaded_files)} File(s)", type="primary"):
            progress_bar = st.progress(0.0, text=f"Processing {len(uploaded_files)} file(s)...")
            status_text = st.empty()
            total_chunks = 0
            n_files = len(uploaded_files)

            try:
                for file_idx, up_file in enumerate(uploaded_files):
                    file_ticker = detect_ticker_from_filename(up_file.name) or default_ticker
                    status_text.info(f"Reading {up_file.name} ({file_ticker}) — file {file_idx + 1} of {n_files}...")
                    text = extract_text(up_file, up_file.name)
                    if not text.strip():
                        continue

                    def on_progress(current, total, msg):
                        file_fraction = (file_idx + (current / max(total, 1))) / n_files
                        progress_bar.progress(min(0.99, file_fraction), text=f"[{file_idx + 1}/{n_files}] {msg}")

                    chunks = ingest_document_text(
                        text=text,
                        filename=up_file.name,
                        ticker=file_ticker,
                        progress_callback=on_progress,
                    )
                    total_chunks += chunks

                progress_bar.progress(1.0, text="Indexing complete.")
                status_text.empty()

                if total_chunks > 0:
                    st.success(f"Successfully indexed {total_chunks} text chunks from {n_files} document(s).")
                    st.rerun()
                else:
                    st.warning("Could not extract readable text from the uploaded files.")
            except Exception as exc:
                progress_bar.empty()
                status_text.empty()
                st.error(f"Error during document ingestion: {exc}")

    st.divider()

    # Knowledge Base Status
    st.subheader("Knowledge Base Status (ChromaDB)")
    kb_summary = get_indexed_summary()
    if kb_summary:
        total_companies = len(kb_summary)
        total_docs = sum(len(s["documents"]) for s in kb_summary)
        total_chunks = sum(s["total_chunks"] for s in kb_summary)

        m1, m2, m3 = st.columns(3)
        m1.metric("Indexed Companies", total_companies)
        m2.metric("Documents Stored", total_docs)
        m3.metric("Vector Chunks", total_chunks)

        st.write("##### Company Document Breakdown")
        for s in kb_summary:
            c_ticker = s["ticker"]
            c_docs = s["documents"]
            c_chunks = s["total_chunks"]
            with st.expander(f"{c_ticker} — {c_chunks} chunks ({len(c_docs)} document{'s' if len(c_docs) > 1 else ''})"):
                for doc_name, doc_count in c_docs.items():
                    st.write(f"- `{doc_name}`: {doc_count} chunks")

        with st.expander("Vector Database Maintenance"):
            st.warning("Resetting the database will permanently delete all indexed document chunks.")
            confirm_reset = st.checkbox("Confirm database reset", key="chk_clear_store")
            if st.button("Clear ChromaDB Store", type="secondary", disabled=not confirm_reset):
                if clear_vector_store():
                    st.success("Vector database successfully cleared.")
                    st.rerun()
                else:
                    st.error("Failed to clear vector store.")
    else:
        st.info("No documents currently indexed. Upload SEC filings above to populate the database.")


# -------------------------------------------------------------
# Tab 2: Research & Analysis
# -------------------------------------------------------------
with tab_analysis:
    st.subheader("Research Target")

    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Target Stock Ticker", value="AAPL").upper().strip()
    with col2:
        benchmark = st.text_input("Benchmark Competitor Ticker", value="MSFT").upper().strip()

    indexed_tickers = get_indexed_tickers()
    if indexed_tickers:
        st.caption("Indexed Filings Available: " + " • ".join(f"`{t}`" for t in indexed_tickers))

    # Knowledge base status check
    is_indexed = is_ticker_indexed(ticker)
    if is_indexed:
        st.success(f"SEC filing data is available for {ticker} in the local vector store.")
    else:
        st.warning(f"No indexed filings found for {ticker}. The research agent will rely on live market data unless a filing is uploaded.")
        with st.expander(f"Quick upload filing for {ticker}"):
            inline_file = st.file_uploader(
                f"Select filing (.txt or .pdf) for {ticker}",
                type=["txt", "pdf"],
                key=f"inline_uploader_{ticker}",
            )
            if inline_file is not None:
                if st.button(f"Save {inline_file.name}", key=f"btn_index_{ticker}"):
                    with st.spinner(f"Processing {inline_file.name}..."):
                        try:
                            text = extract_text(inline_file, inline_file.name)
                            chunks = ingest_document_text(text, inline_file.name, ticker)
                            if chunks > 0:
                                st.success(f"Indexed {chunks} chunks for {ticker}.")
                                st.rerun()
                            else:
                                st.error("No text could be extracted from this file.")
                        except Exception as e:
                            st.error(f"Error processing file: {e}")

    # Market Price History
    st.subheader("Market Price Overview")
    _, m_period_col = st.columns([3, 1])
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
        st.line_chart(history_df["Close"], use_container_width=True)
    else:
        st.caption(f"No price history available for {ticker}.")

    st.divider()

    # Research Execution
    if st.button(f"Run Research Pipeline on {ticker}", type="primary", use_container_width=True):
        workflow = WorkflowService()
        bench_val = benchmark if benchmark else ("MSFT" if ticker != "MSFT" else "GOOGL")
        thread_id = f"research_{ticker}_{int(time.time())}"
        initial_input = {"ticker": ticker, "benchmark": bench_val}
        state = dict(initial_input)

        with st.status(f"Executing multi-agent research for {ticker} vs. {bench_val}...", expanded=True) as status_box:
            st.write("Initializing workflow parameters...")
            for step in workflow.stream(initial_input, thread_id=thread_id):
                for node_name, updated_state in step.items():
                    if node_name == "__interrupt__":
                        st.write("⏸️ Paused at Human-in-the-Loop review gate.")
                    elif isinstance(updated_state, dict):
                        state.update(updated_state)
                        if node_name == "router":
                            st.write(f"• Target symbol: `{ticker}`, Benchmark: `{bench_val}`")
                        elif node_name == "market_research":
                            st.write("• Extracted 10-K financial fundamentals via vector retrieval")
                        elif node_name == "trend_analysis":
                            st.write("• Gathered market sentiment and sector trends")
                        elif node_name == "comparative_analysis":
                            st.write(f"• Completed peer comparative valuation vs. {bench_val}")
                        elif node_name == "summary_agent":
                            st.write("• Drafted investment thesis and risk assessment")

            status_box.update(label=f"Research pipeline completed for {ticker}", state="complete", expanded=False)
            st.session_state["workflow"] = workflow
            st.session_state["thread_id"] = thread_id
            st.session_state["latest_research"] = state
            st.session_state["awaiting_approval"] = True

        st.info("The research workflow has paused for human review. Please switch to the **Analyst Review (HITL)** tab to inspect or approve the thesis.")

        # Display Fundamentals
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
            st.subheader("Fundamental Analysis Summary")
            st.write(summary)

        # Display Sentiment & Sector Trends
        sentiment = state.get("sentiment", {})
        if sentiment:
            st.subheader("Market Sentiment & Sector Trends")
            s_col1, s_col2 = st.columns(2)
            sentiment_label = sentiment.get("label", "Neutral")
            with s_col1:
                st.metric("Sentiment", sentiment_label)
            with s_col2:
                score = sentiment.get("score", 0.0)
                st.metric("Confidence Score", f"{score:+.2f}")

            if sentiment.get("summary"):
                st.write(sentiment.get("summary"))

            col_tail, col_risk = st.columns(2)
            with col_tail:
                tailwinds = sentiment.get("sector_tailwinds", [])
                if tailwinds:
                    st.write("**Sector Catalysts & Tailwinds:**")
                    for item in tailwinds:
                        st.write(f"- {item}")
            with col_risk:
                macro_risks = sentiment.get("macro_risks", [])
                if macro_risks:
                    st.write("**Macro & Market Risks:**")
                    for item in macro_risks:
                        st.write(f"- {item}")

        # Display Peer Comparison
        comparison = state.get("comparison", {})
        if comparison:
            bench_ticker = comparison.get("benchmark_ticker", "Peer")
            st.subheader(f"Peer Comparison ({ticker} vs. {bench_ticker})")

            verdict = comparison.get("verdict", "")
            if verdict:
                st.info(f"**Comparative Verdict:** {verdict}")

            rel_summary = comparison.get("relative_valuation_summary", "")
            if rel_summary:
                st.write(rel_summary)

            multiples = comparison.get("multiples", [])
            if multiples:
                rows = []
                for m in multiples:
                    rows.append({
                        "Metric": m.get("metric"),
                        ticker: m.get("target_value"),
                        bench_ticker: m.get("benchmark_value"),
                        "Advantage": m.get("advantage"),
                    })
                st.dataframe(rows, use_container_width=True)

            c_adv, c_vuln = st.columns(2)
            with c_adv:
                advantages = comparison.get("target_advantages", [])
                if advantages:
                    st.write(f"**Competitive Strengths:**")
                    for adv in advantages:
                        st.write(f"- {adv}")
            with c_vuln:
                vulns = comparison.get("target_vulnerabilities", [])
                if vulns:
                    st.write(f"**Vulnerabilities vs. {bench_ticker}:**")
                    for vuln in vulns:
                        st.write(f"- {vuln}")

        # Display Filing Risk Factors
        if risks:
            st.subheader("SEC Filing Risk Factors")
            for r in risks:
                st.write(f"- {r}")

        # Display Draft Thesis
        draft = state.get("draft_thesis", {})
        if draft:
            st.subheader("Draft Investment Thesis")
            rating = draft.get("rating", state.get("rating", "HOLD"))
            target_p = draft.get("target_price", state.get("target_price", "N/A"))
            upside = draft.get("upside_potential_pct", "N/A")
            vol_metrics = draft.get("volatility_metrics", {})

            col_r, col_tp, col_up, col_vol = st.columns(4)
            col_r.metric("Rating", rating)
            col_tp.metric("Target Price", f"${target_p}")
            col_up.metric("Est. Upside", f"{upside}%" if upside != "N/A" else "N/A")
            ann_vol_val = vol_metrics.get("annualized_volatility_pct", "N/A")
            col_vol.metric("6M Realized Volatility", f"{ann_vol_val}%" if ann_vol_val != "N/A" else "N/A")

            exec_sum = draft.get("executive_summary", "")
            if exec_sum:
                st.write(f"**Executive Summary:** {exec_sum}")

            t_cols = st.columns(3)
            with t_cols[0]:
                st.write("**Core Thesis Points:**")
                for tp in draft.get("thesis_points", []):
                    st.write(f"- {tp}")
            with t_cols[1]:
                st.write("**Identified Risks:**")
                for rk in draft.get("key_risks", []):
                    st.write(f"- {rk}")
            with t_cols[2]:
                st.write("**Catalysts:**")
                for cat in draft.get("catalysts", []):
                    st.write(f"- {cat}")


# -------------------------------------------------------------
# Tab 3: Analyst Review (HITL)
# -------------------------------------------------------------
with tab_review:
    st.subheader("Analyst Review & Sign-Off Gate")

    latest = st.session_state.get("latest_research")
    if not latest or not latest.get("draft_thesis"):
        st.info("No research report available to review yet. Run an analysis from the 'Research & Analysis' tab first.")
    else:
        ticker = latest.get("ticker", "AAPL")
        draft = latest.get("draft_thesis", {})
        benchmark = latest.get("benchmark", "MSFT")
        is_awaiting = st.session_state.get("awaiting_approval", False)
        is_approved = latest.get("approved")
        feedback = latest.get("feedback")

        if is_awaiting:
            st.warning("⚠️ **Status: Awaiting Analyst Review.** The workflow has paused at the human review gate before finalizing the memo.")
        elif is_approved is True:
            st.success("✅ **Status: Approved.** The thesis was certified by the analyst.")
            if feedback:
                st.caption(f"Analyst Notes: {feedback}")
        elif is_approved is False:
            st.error("⚠️ **Status: Revisions Requested.** The analyst flagged concerns with this thesis.")
            if feedback:
                st.caption(f"Feedback: {feedback}")

        # Summary Metrics
        rating = draft.get("rating", latest.get("rating", "HOLD"))
        target_p = draft.get("target_price", latest.get("target_price", "N/A"))
        upside = draft.get("upside_potential_pct", "N/A")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ticker", ticker)
        c2.metric("Proposed Rating", rating)
        c3.metric("Target Price", f"${target_p}")
        c4.metric("Est. Upside", f"{upside}%" if upside != "N/A" else "N/A")

        exec_sum = draft.get("executive_summary", "")
        if exec_sum:
            st.write(f"**Executive Summary:** {exec_sum}")

        col_tp, col_rk = st.columns(2)
        with col_tp:
            st.write("**Thesis Points:**")
            for tp in draft.get("thesis_points", []):
                st.write(f"- {tp}")
        with col_rk:
            st.write("**Risk Factors:**")
            for rk in draft.get("key_risks", []):
                st.write(f"- {rk}")

        st.divider()

        # Review Form
        st.subheader("Analyst Decision")
        with st.form("hitl_review_form"):
            decision = st.radio(
                "Select action:",
                ["Approve Investment Thesis", "Request Revisions / Flag Concerns"],
                index=0 if (is_approved is not False) else 1,
            )
            analyst_notes = st.text_area(
                "Analyst Feedback / Notes:",
                value=feedback if feedback else "",
                placeholder="Enter feedback or validation notes here...",
            )
            submit_btn = st.form_submit_button("Submit Decision", type="primary")

            if submit_btn:
                approve_decision = (decision == "Approve Investment Thesis")
                wf = st.session_state.get("workflow")
                th_id = st.session_state.get("thread_id")
                if wf and th_id:
                    try:
                        res = wf.resume({"approved": approve_decision, "feedback": analyst_notes}, thread_id=th_id)
                        if isinstance(res, dict):
                            latest.update(res)
                    except Exception:
                        latest["approved"] = approve_decision
                        latest["feedback"] = analyst_notes
                else:
                    latest["approved"] = approve_decision
                    latest["feedback"] = analyst_notes

                latest["approved"] = approve_decision
                latest["feedback"] = analyst_notes
                st.session_state["latest_research"] = latest
                st.session_state["awaiting_approval"] = False
                st.toast("Decision recorded successfully.")
                st.rerun()
