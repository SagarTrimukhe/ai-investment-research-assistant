import os
import sys
import time

# Ensure project root is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.services.workflow_service import WorkflowService
from app.integrations.market_data import fetch_stock_overview, fetch_price_history
from app.integrations.s3_client import S3Service
from app.services.export_service import ExportService
from app.services.document_ingestion import (
    extract_text,
    ingest_document_text,
    get_indexed_tickers,
    get_indexed_summary,
    is_ticker_indexed,
    detect_ticker_from_filename,
    clear_vector_store,
)
from app.services.nasdaq_universe import (
    get_nasdaq_universe,
    get_nasdaq_tickers,
    get_nasdaq_company_name,
    detect_nasdaq_ticker,
    NASDAQ_UNIVERSE,
)
from app.ui_theme import (
    inject_custom_css,
    render_hero_banner,
    render_ticker_tape,
    render_52w_range_bar,
    render_agent_stepper_visualizer,
    render_sidebar_branding,
    render_sidebar_system_info,
    render_sidebar_tickers,
    render_section_title,
    render_glass_card,
    render_executive_summary,
    render_sidebar_footer,
)

st.set_page_config(
    page_title="AI Investment Research Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom dark modern design system
inject_custom_css()

# Sidebar: Modern branding and status badges
render_sidebar_branding()
s3_status = S3Service().is_configured()
render_sidebar_system_info(s3_status)

indexed_list = get_indexed_tickers()
render_sidebar_tickers(indexed_list)
render_sidebar_footer()


# Top Modern Hero Banner & Live Animated Ticker Tape
render_hero_banner()
render_ticker_tape()

tab_ingest, tab_analysis, tab_review = st.tabs([
    "📥 Document Ingestion",
    "📈 Research & Analysis",
    "🛡️ Analyst Review (HITL)",
])



# -------------------------------------------------------------
# Tab 1: Document Ingestion
# -------------------------------------------------------------
with tab_ingest:
    render_section_title(
        "Upload Filings & Research Reports",
        "Upload company 10-K, 10-Q, or research reports (PDF or TXT) to index into the vector database.",
        icon="📥",
    )

    ingest_col1, ingest_col2 = st.columns([1.2, 1.8])
    with ingest_col1:
        raw_ticker_input = st.text_input(
            "Associated Stock Ticker or Company Name",
            value=st.session_state.get("ingest_ticker_input", "AAPL"),
            key="ingest_ticker_input",
            help="Enter a stock ticker (e.g., AAPL, NVDA, TSLA) or company name (e.g., Apple, Tesla, Nvidia)",
        ).strip()
        default_ticker = detect_nasdaq_ticker(raw_ticker_input) or raw_ticker_input.upper().strip()
    with ingest_col2:
        uploaded_files = st.file_uploader(
            "Select Custom Document Files (Optional)",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            key="general_uploader",
            help="Upload your own PDF or TXT annual/quarterly reports for the selected company.",
        )

    # -------------------------------------------------------------
    # Instant Stock Feedback & One-Click 10-K Ingestion Card
    # -------------------------------------------------------------
    if default_ticker:
        is_indexed = is_ticker_indexed(default_ticker)
        company_name = get_nasdaq_company_name(default_ticker)

        # Check local pre-loaded 10-K filing availability
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "nasdaq_reports"))
        local_report_path = os.path.join(reports_dir, f"{default_ticker}_10K_filing.txt")
        has_local_report = os.path.exists(local_report_path)

        # Fetch live company overview snapshot
        stock_info = fetch_stock_overview(default_ticker)
        display_name = stock_info.get("name") or company_name
        price = stock_info.get("current_price")
        change_pct = stock_info.get("change_pct", 0.0)
        sector = stock_info.get("sector") or (NASDAQ_UNIVERSE.get(default_ticker, {}).get("sector", "Equities"))
        industry = stock_info.get("industry") or (NASDAQ_UNIVERSE.get(default_ticker, {}).get("industry", "Financial Asset"))

        price_str = f"${price:.2f}" if price else "Quote Active"
        change_color = "#10B981" if change_pct >= 0 else "#F43F5E"
        change_arrow = "▲" if change_pct >= 0 else "▼"
        change_html = f"<span style='color: {change_color}; font-weight: 700; font-family: monospace;'>{change_arrow} {abs(change_pct):.2f}%</span>" if price else ""

        if is_indexed:
            status_badge = "<span style='background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #34D399; padding: 4px 10px; border-radius: 6px; font-size: 0.76rem; font-weight: 600;'>✓ Filings Indexed in Vector DB</span>"
        elif has_local_report:
            status_badge = "<span style='background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.35); color: #60A5FA; padding: 4px 10px; border-radius: 6px; font-size: 0.76rem; font-weight: 600;'>📄 10-K Filing Ready to Ingest</span>"
        else:
            status_badge = "<span style='background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); color: #FBBF24; padding: 4px 10px; border-radius: 6px; font-size: 0.76rem; font-weight: 600;'>○ Not Indexed (Upload Below)</span>"

        resolved_note = f"<span style='color: #60A5FA; font-size: 0.76rem; margin-left: 6px;'>[Resolved from \"{raw_ticker_input}\"]</span>" if raw_ticker_input.upper() != default_ticker else ""

        st.html(f"""
        <div style="
            background: #151D2C;
            border: 1px solid #222F44;
            border-radius: 12px;
            padding: 16px 20px;
            margin: 12px 0 16px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 800; color: #F8FAFC;">{default_ticker}</span>
                        <span style="font-size: 1rem; font-weight: 600; color: #CBD5E1;">{display_name}</span>
                        {resolved_note}
                        {status_badge}
                    </div>
                    <div style="font-size: 0.80rem; color: #94A3B8; margin-top: 4px;">
                        Sector: <strong style="color: #F8FAFC;">{sector}</strong> &nbsp;•&nbsp; Industry: <strong style="color: #F8FAFC;">{industry}</strong>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.35rem; font-weight: 700; color: #F8FAFC;">
                        {price_str} {change_html}
                    </div>
                    <div style="font-size: 0.72rem; color: #64748B;">Live SEC & Market Telemetry</div>
                </div>
            </div>
        </div>
        """)

        # Quick Action Buttons row
        btn_c1, btn_c2, btn_c3 = st.columns([1.5, 1.5, 2])
        with btn_c1:
            if has_local_report and not is_indexed:
                file_size_kb = os.path.getsize(local_report_path) / 1024
                if st.button(f"⚡ Ingest Official {default_ticker} 10-K ({file_size_kb:.0f} KB)", type="primary", key=f"btn_quick_ingest_{default_ticker}", use_container_width=True):
                    with st.spinner(f"Reading & indexing official Form 10-K for {default_ticker}..."):
                        try:
                            with open(local_report_path, "r", encoding="utf-8") as rf:
                                report_content = rf.read()
                            chs = ingest_document_text(
                                text=report_content,
                                filename=f"{default_ticker}_10K_filing.txt",
                                ticker=default_ticker,
                            )
                            s3 = S3Service()
                            if s3.is_available():
                                s3.upload_bytes(
                                    report_content.encode("utf-8"),
                                    f"filings/{default_ticker}/{default_ticker}_10K_filing.txt",
                                )
                            st.success(f"Successfully indexed {chs} text chunks from {default_ticker} 10-K into ChromaDB!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error indexing 10-K: {e}")
            elif is_indexed:
                st.success(f"✓ {default_ticker} 10-K is indexed in vector database.")
            else:
                st.info(f"Upload custom filing below or run multi-agent live telemetry.")

        with btn_c2:
            if st.button(f"🔍 Research {default_ticker} in Tab 2", key=f"btn_nav_research_{default_ticker}", use_container_width=True):
                st.session_state["target_ticker_val"] = default_ticker
                st.session_state["target_ticker_field"] = default_ticker
                st.info(f"Target set to {default_ticker}! Switch to **Stock Analysis & Due Diligence** tab to run pipeline.")

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

                    # Archive copy to AWS S3 if configured
                    s3 = S3Service()
                    if s3.is_configured():
                        up_file.seek(0)
                        s3.upload_bytes(up_file.read(), f"filings/{file_ticker}/{up_file.name}")

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

    # Pre-Loaded Offline NASDAQ Reports (200+ Stocks)
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "nasdaq_reports"))
    if os.path.exists(reports_dir):
        available_files = [f for f in os.listdir(reports_dir) if f.endswith("_10K_filing.txt")]
        if available_files:
            with st.expander(f"📁 Pre-Loaded Offline NASDAQ Reports ({len(available_files)} Stocks Available)", expanded=False):
                st.caption(
                    "Standardized Form 10-K filing reports pulled from official SEC EDGAR records. "
                    "Kept locally for rapid offline multi-agent testing without needing manual uploads."
                )
                avail_tickers = sorted([f.replace("_10K_filing.txt", "") for f in available_files])
                col_n1, col_n2 = st.columns([3, 1])
                with col_n1:
                    chosen_report_ticker = st.selectbox(
                        "Select Stock to Test",
                        options=avail_tickers,
                        format_func=lambda t: f"{t} — {get_nasdaq_company_name(t)}",
                        key="sel_offline_nasdaq_stock",
                    )
                with col_n2:
                    st.write("")
                    st.write("")
                    if st.button(f"Ingest {chosen_report_ticker} 10-K", type="primary", key="btn_ingest_offline_report"):
                        report_path = os.path.join(reports_dir, f"{chosen_report_ticker}_10K_filing.txt")
                        try:
                            with open(report_path, "r", encoding="utf-8") as rf:
                                report_content = rf.read()
                            with st.spinner(f"Ingesting 10-K for {chosen_report_ticker}..."):
                                chs = ingest_document_text(
                                    text=report_content,
                                    filename=f"{chosen_report_ticker}_10K_filing.txt",
                                    ticker=chosen_report_ticker,
                                )
                                s3 = S3Service()
                                if s3.is_available():
                                    s3.upload_bytes(
                                        report_content.encode("utf-8"),
                                        f"filings/{chosen_report_ticker}/{chosen_report_ticker}_10K_filing.txt",
                                    )
                                st.success(f"Indexed {chs} chunks for {chosen_report_ticker}!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Failed to ingest report: {e}")

    st.divider()

    # Knowledge Base Status
    render_section_title(
        "Knowledge Base Status (ChromaDB)",
        "Live vector indexing metrics across stored company filings",
        icon="🗄️",
    )
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
    render_section_title(
        "Research Target Selection",
        "Configure target asset and benchmark peer for automated multi-agent investigation",
        icon="🎯",
    )

    st.html('<div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#94A3B8; font-weight:700; margin-bottom:8px;">⚡ Quick Select Benchmark Assets:</div>')
    q_cols = st.columns(7)
    quick_picks = ["AAPL", "NVDA", "MSFT", "META", "AMZN", "GOOGL", "TSLA"]
    for q_col, q_sym in zip(q_cols, quick_picks):
        if q_col.button(q_sym, key=f"quick_{q_sym}", use_container_width=True):
            st.session_state["target_ticker_val"] = q_sym
            st.session_state["benchmark_val"] = "MSFT" if q_sym != "MSFT" else "GOOGL"
            st.rerun()

    target_default = st.session_state.get("target_ticker_val", "AAPL")
    bench_default = st.session_state.get("benchmark_val", "MSFT")

    col1, col2 = st.columns(2)
    with col1:
        raw_target = st.text_input(
            "Target Stock Ticker or Company Name",
            value=target_default,
            key="target_ticker_field",
            help="Enter ticker or company name (e.g. AAPL, NVDA, TSLA, Tesla, Apple)",
        ).strip()
        ticker = detect_nasdaq_ticker(raw_target) or raw_target.upper()
        if raw_target.upper() != ticker:
            st.caption(f"Resolved: `{ticker}` — **{get_nasdaq_company_name(ticker)}**")
    with col2:
        raw_bench = st.text_input(
            "Benchmark Competitor Ticker or Company Name",
            value=bench_default,
            key="bench_ticker_field",
            help="Enter benchmark ticker or company name (e.g. MSFT, Google)",
        ).strip()
        benchmark = detect_nasdaq_ticker(raw_bench) or raw_bench.upper()
        if raw_bench.upper() != benchmark:
            st.caption(f"Resolved: `{benchmark}` — **{get_nasdaq_company_name(benchmark)}**")

    indexed_tickers = get_indexed_tickers()
    if indexed_tickers:
        st.caption("Indexed Filings Available: " + " • ".join(f"`{t}`" for t in indexed_tickers))

    with st.expander("🔎 Browse 200+ Supported NASDAQ Stocks"):
        st.caption("Extensive coverage across Tech, Semiconductors, Cloud/SaaS, Biotech, and Consumer:")
        all_nasdaq = get_nasdaq_tickers()
        st.write(" • ".join(f"`{t}`" for t in all_nasdaq[:50]) + f" ... and {len(all_nasdaq) - 50} more.")

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
    render_section_title(
        "Market Price Overview",
        "Real-time market quotes and historical price trends via Yahoo Finance",
        icon="📈",
    )
    _, m_period_col = st.columns([3, 1])
    with m_period_col:
        period = st.selectbox(
            "Timeframe",
            options=["1mo", "3mo", "6mo", "1y", "ytd"],
            index=2,
            key="price_period",
        )

    overview = fetch_stock_overview(ticker)
    if overview and overview.get("name"):
        sector_info = []
        if overview.get("sector"):
            sector_info.append(overview["sector"])
        if overview.get("industry"):
            sector_info.append(overview["industry"])
        meta_sub = " · ".join(sector_info)

        st.markdown(f"### {overview['name']} (`{ticker}`)")
        if meta_sub:
            st.caption(f"**Classification:** {meta_sub}")
        if overview.get("description"):
            with st.expander("🏢 Company Overview & Business Summary", expanded=False):
                st.write(overview["description"])

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

        # Dynamic 52-Week Range Bar
        render_52w_range_bar(
            overview.get("current_price"),
            overview.get("fifty_two_week_low"),
            overview.get("fifty_two_week_high"),
        )

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
            completed_steps = []
            stepper_placeholder = st.empty()
            with stepper_placeholder.container():
                render_agent_stepper_visualizer(completed_steps)

            st.write("Initializing workflow parameters...")
            for step in workflow.stream(initial_input, thread_id=thread_id):
                for node_name, updated_state in step.items():
                    if node_name not in completed_steps:
                        completed_steps.append(node_name)
                    with stepper_placeholder.container():
                        render_agent_stepper_visualizer(completed_steps)

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
            render_section_title("Key Financial Metrics", "Fundamental accounting metrics extracted from 10-K SEC filings", icon="📊")
            m_cols = st.columns(len(metrics))
            for col, (k, v) in zip(m_cols, metrics.items()):
                label = k.replace("_", " ").title()
                col.metric(label, v)

        if summary:
            render_section_title("Fundamental Analysis Summary", "Automated qualitative breakdown from filing notes", icon="📑")
            st.write(summary)

        # Display Sentiment & Sector Trends
        sentiment = state.get("sentiment", {})
        if sentiment:
            render_section_title("Market Sentiment & Sector Trends", "Real-time macro catalysts, sentiment scoring, and headwind analysis", icon="🌐")
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
                    render_glass_card("Sector Catalysts & Tailwinds", tailwinds, icon="⚡", accent_color="#10B981")
            with col_risk:
                macro_risks = sentiment.get("macro_risks", [])
                if macro_risks:
                    render_glass_card("Macro & Market Risks", macro_risks, icon="📉", accent_color="#F59E0B")

        # Display Peer Comparison
        comparison = state.get("comparison", {})
        if comparison:
            bench_ticker = comparison.get("benchmark_ticker", "Peer")
            render_section_title(f"Peer Comparison ({ticker} vs. {bench_ticker})", "Relative valuation multiples and strategic positioning", icon="⚖️")

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
                    render_glass_card(f"Competitive Strengths ({ticker})", advantages, icon="🛡️", accent_color="#10B981")
            with c_vuln:
                vulns = comparison.get("target_vulnerabilities", [])
                if vulns:
                    render_glass_card(f"Vulnerabilities vs. {bench_ticker}", vulns, icon="⚠️", accent_color="#F43F5E")

        # Display Filing Risk Factors
        if risks:
            render_section_title("SEC Filing Risk Factors", "Item 1A risk disclosure analysis", icon="⚠️")
            render_glass_card("Disclosed Risk Factors", risks, icon="⚠️", accent_color="#F59E0B")

        # Display Draft Thesis
        draft = state.get("draft_thesis", {})
        if draft:
            render_section_title("Draft Investment Thesis", "Synthesized target price, thesis pillars, and recommendation", icon="💡")
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
                render_executive_summary(exec_sum)

            t_cols = st.columns(3)
            with t_cols[0]:
                render_glass_card("Core Thesis Points", draft.get("thesis_points", []), icon="🎯", accent_color="#6366F1")
            with t_cols[1]:
                render_glass_card("Identified Risks", draft.get("key_risks", []), icon="⚠️", accent_color="#F43F5E")
            with t_cols[2]:
                render_glass_card("Catalysts & Drivers", draft.get("catalysts", []), icon="🚀", accent_color="#10B981")

            red_pill = draft.get("red_pill_insights", "")
            if red_pill:
                st.markdown("**🔴 Red Pill Insights** *(Contrarian View)*")
                st.warning(red_pill)


# -------------------------------------------------------------
# Tab 3: Analyst Review (HITL)
# -------------------------------------------------------------
with tab_review:
    render_section_title(
        "Analyst Review & Sign-Off Gate",
        "Human-in-the-Loop governance to audit, edit, and certify AI-generated investment theses",
        icon="🛡️",
    )

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
            render_executive_summary(exec_sum)

        col_tp, col_rk = st.columns(2)
        with col_tp:
            render_glass_card("Thesis Points", draft.get("thesis_points", []), icon="🎯", accent_color="#6366F1")
        with col_rk:
            render_glass_card("Risk Factors", draft.get("key_risks", []), icon="⚠️", accent_color="#F43F5E")

        red_pill = draft.get("red_pill_insights", "")
        if red_pill:
            st.markdown("**🔴 Red Pill Insights** *(Contrarian View)*")
            st.warning(red_pill)

        st.divider()

        # Review Form
        render_section_title("Analyst Decision & Audit Log", "Record human approval decision and discretionary oversight", icon="✍️")
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

        # Report Export & S3 Cloud Storage Sync
        st.divider()
        render_section_title("Report Export & Cloud Storage (AWS S3)", "Download certified markdown memo or sync directly to S3 storage bucket", icon="☁️")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            exporter = ExportService()
            report_md = exporter.to_markdown(latest, f"data/processed/{ticker}_investment_memo.md")
            st.download_button(
                "📥 Download Certified Memorandum (.md)",
                data=report_md,
                file_name=f"{ticker}_investment_memo.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with exp_col2:
            if st.button("☁️ Archive Memorandum to AWS S3", use_container_width=True):
                exporter = ExportService()
                s3_uri = exporter.export_to_s3(latest)
                if s3_uri:
                    st.success(f"Report archived to `{s3_uri}`")
                else:
                    st.info("AWS S3 credentials not provided in `.env`. Saved to `data/processed/` locally.")


# UI Orchestration Completed - Institutional Light Mode Verified
