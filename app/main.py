import os
import sys

# ensure project root is on python path regardless of how streamlit is launched
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

# ── Custom CSS for polished UI ──
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

/* ── Main title area ── */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
}
.main-header h1 {
    color: #fff;
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: rgba(255,255,255,0.8);
    font-size: 0.95rem;
    margin: 0.3rem 0 0;
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #e0e0e0;
    font-size: 0.88rem;
}
section[data-testid="stSidebar"] h2 {
    color: #e0e0e0 !important;
    font-size: 1.1rem !important;
}

/* ── Status pill badges ── */
.status-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.pill-green {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.pill-blue {
    background: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
    border: 1px solid rgba(59, 130, 246, 0.3);
}
.pill-amber {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* ── Info card ── */
.info-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.08));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
}
.info-card h4 {
    margin: 0 0 0.3rem;
    font-size: 0.85rem;
    color: #a5b4fc;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.info-card .value {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e0e7ff;
}

/* ── Indexed ticker chip ── */
.ticker-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(52,211,153,0.08));
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 10px;
    padding: 10px 18px;
    margin: 4px;
    font-weight: 600;
    color: #34d399;
    font-size: 0.9rem;
}

/* ── Section heading with accent bar ── */
.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem 0 0.8rem;
}
.section-heading .accent-bar {
    width: 4px;
    height: 24px;
    background: linear-gradient(180deg, #667eea, #764ba2);
    border-radius: 2px;
}
.section-heading h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
}

/* ── Knowledge base status banner ── */
.kb-status {
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.9rem;
}
.kb-ready {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.25);
    color: #34d399;
}
.kb-missing {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.25);
    color: #fbbf24;
}
.kb-status .icon { font-size: 1.3rem; }
.kb-status .text { flex: 1; }
.kb-status .text strong { color: #f1f5f9; }

/* ── Metric cards override ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

/* ── Hide the default Streamlit header/footer ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 0.5rem;">
        <div style="font-size: 2.2rem;">📊</div>
        <div style="font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin-top: 0.2rem;">
            Dashboard
        </div>
        <div style="font-size: 0.72rem; color: rgba(255,255,255,0.5);">
            Powered by Gemini + LangChain + ChromaDB
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Combined system status card
    st.markdown("""
    <div class="info-card" style="padding: 0.8rem 1rem; margin-bottom: 0.8rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.75rem; color:#94a3b8; font-weight:600; text-transform:uppercase;">🤖 LLM</span>
            <span class="status-pill pill-green">Gemini 1.5 Flash</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.75rem; color:#94a3b8; font-weight:600; text-transform:uppercase;">🗄️ Vector DB</span>
            <span class="status-pill pill-blue">ChromaDB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Indexed companies
    indexed_list = get_indexed_tickers()
    st.markdown(f"""
    <div class="section-heading" style="margin-bottom: 8px;">
        <div class="accent-bar"></div>
        <h3 style="font-size:0.95rem;">Indexed Companies ({len(indexed_list)})</h3>
    </div>
    """, unsafe_allow_html=True)

    if indexed_list:
        chips_html = "".join(
            f'<span class="ticker-chip" style="margin:2px;">📈 {t}</span>' for t in indexed_list
        )
        st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">{chips_html}</div>', unsafe_allow_html=True)
    else:
        st.caption("No filings indexed yet.")

    st.divider()
    st.caption("Theme 15 • Built with LangChain + Gemini + ChromaDB")


# ── Main content header ──
st.markdown("""
<div class="main-header">
    <h1>📊 AI Stock Research Helper</h1>
    <p>Upload company reports and let AI research agents extract insights for you!</p>
</div>
""", unsafe_allow_html=True)

tab_ingest, tab_analysis, tab_review = st.tabs([
    "📁 Upload Documents",
    "🔬 Run Analysis",
    "✅ Review Results",
])


# ═══════════════════════════════════════════════════════
# TAB 1 — Document Ingestion
# ═══════════════════════════════════════════════════════
with tab_ingest:
    # ── Educational Guide for Students / First-time Users ──
    with st.expander("💡 **New here? Click to learn how this works!**", expanded=False):
        st.markdown("""
        **Hey! Here's a quick walkthrough 👋**

        **What's a Stock Ticker?**
        It's just a short code for a company — like `AAPL` = Apple, `NVDA` = Nvidia, `META` = Meta/Facebook, `INFY` = Infosys.

        **What happens when you upload a file?**
        1. We read the text from your PDF/TXT file
        2. Break it into smaller paragraphs (we call them "chunks")
        3. Convert each chunk into numbers ("embeddings") using Google Gemini AI
        4. Save everything into our ChromaDB database tagged with the company name

        **Why do we do this?**
        So when you go to the **🔬 Run Analysis** tab and ask our AI to research a stock, it can look up real data from the actual company filings instead of just making stuff up!

        **What's next after uploading?**
        Once your files show up below, head over to **🔬 Run Analysis** and hit the research button!
        """)

    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Upload Company Reports</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Drop any company report here (.pdf or .txt) — we'll figure out which stock it belongs to from the filename!")

    ingest_col1, ingest_col2 = st.columns([1, 2])
    with ingest_col1:
        default_ticker = st.text_input(
            "🏷️ Stock Code",
            value="AAPL",
            key="ingest_ticker_input",
            help="If we can't figure out the company from the filename, we'll use this as default.",
        ).upper().strip()
    with ingest_col2:
        uploaded_files = st.file_uploader(
            "📎 Drop your files here",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            key="general_uploader",
        )

    if uploaded_files:
        st.markdown("##### 📋 Here's what we found in your files")
        preview_rows = []
        for up_file in uploaded_files:
            detected = detect_ticker_from_filename(up_file.name) or default_ticker
            preview_rows.append({
                "Document Name": up_file.name,
                "Assigned Stock": detected,
                "Size": f"{len(up_file.getvalue()) / 1024:.1f} KB",
                "How we knew": "Figured it out from filename ✨" if detect_ticker_from_filename(up_file.name) else f"Using your default: {default_ticker}",
            })
        st.dataframe(preview_rows, use_container_width=True)

        if st.button(f"🚀 Upload & Save {len(uploaded_files)} File(s) to Database", type="primary", use_container_width=True):
            progress_bar = st.progress(0.0, text=f"Getting {len(uploaded_files)} file(s) ready...")
            status_text = st.empty()
            total_chunks = 0
            n_files = len(uploaded_files)

            try:
                for file_idx, up_file in enumerate(uploaded_files):
                    file_ticker = detect_ticker_from_filename(up_file.name) or default_ticker
                    status_text.info(f"📖 Reading **{up_file.name}** ({file_ticker}) — file {file_idx + 1} of {n_files}...")
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

                progress_bar.progress(1.0, text="✨ All done!")
                status_text.empty()

                if total_chunks > 0:
                    st.success(f"✅ Nice! Saved **{total_chunks} text chunks** from {n_files} file(s) into our database!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Hmm, couldn't read any text from those files. Are they scanned images maybe?")
            except Exception as exc:
                progress_bar.empty()
                status_text.empty()
                err_text = str(exc)
                if "429" in err_text or "quota" in err_text.lower():
                    st.error(
                        f"⏳ **Whoa, too many requests!**\n\n"
                        f"Google's free API only allows 100 requests per minute and we hit that limit.\n\n"
                        f"- We managed to save **{total_chunks}** chunks before it stopped\n"
                        f"- Just wait about **60 seconds** and try again — it'll pick up where it left off\n\n"
                        f"*Pro tip: uploading one file at a time is easier on the free tier!*"
                    )
                else:
                    st.error(f"❌ Something went wrong: {err_text}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── What's in our database ──
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>What's in Our Database So Far</h3>
    </div>
    """, unsafe_allow_html=True)

    kb_summary = get_indexed_summary()
    if kb_summary:
        total_companies = len(kb_summary)
        total_docs = sum(len(s["documents"]) for s in kb_summary)
        total_chunks = sum(s["total_chunks"] for s in kb_summary)

        # 3 stat cards
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🏢 Companies", f"{total_companies}")
        with m2:
            st.metric("📑 Files Stored", f"{total_docs}")
        with m3:
            st.metric("🧩 Text Chunks", f"{total_chunks}")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("##### 📁 Company-wise Details")
        for s in kb_summary:
            c_ticker = s["ticker"]
            c_docs = s["documents"]
            c_chunks = s["total_chunks"]
            with st.expander(f"📈 **{c_ticker}** — {c_chunks} chunks from {len(c_docs)} file{'s' if len(c_docs) > 1 else ''}", expanded=True):
                for doc_name, doc_count in c_docs.items():
                    st.markdown(f"- 📄 `{doc_name}` — {doc_count} chunks saved")

        st.markdown("""
        <div class="kb-status kb-ready" style="margin-top: 1.2rem;">
            <span class="icon">👉</span>
            <span class="text"><strong>You're all set!</strong> Now go to the <strong>🔬 Run Analysis</strong> tab and let the AI agents research these companies for you!</span>
        </div>
        """, unsafe_allow_html=True)

        # Vector store maintenance
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("⚙️ Danger Zone — Reset Database", expanded=False):
            st.warning("⚠️ This will delete everything we've stored. You'll need to re-upload all your files.")
            confirm_reset = st.checkbox("Yes, I'm sure I want to delete everything", key="chk_clear_store")
            if st.button("🗑️ Wipe Database Clean", type="secondary", disabled=not confirm_reset):
                if clear_vector_store():
                    st.success("Database wiped! Upload new files to start fresh.")
                    st.rerun()
                else:
                    st.error("Oops, something went wrong while clearing.")
    else:
        st.info("Nothing here yet! Upload a company report above and we'll store it for analysis.")


# ═══════════════════════════════════════════════════════
# TAB 2 — Research & Analysis
# ═══════════════════════════════════════════════════════
with tab_analysis:
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Pick a Stock to Research</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("🎯 Which stock to analyze?", value="AAPL").upper().strip()
    with col2:
        benchmark = st.text_input("📊 Compare against", value="MSFT").upper().strip()

    indexed_tickers = get_indexed_tickers()
    if indexed_tickers:
        st.caption("💾 **Stocks we have data for:** " + "  •  ".join(f"`{t}`" for t in indexed_tickers))

    # Knowledge base check with styled banner
    is_indexed = is_ticker_indexed(ticker)
    if is_indexed:
        st.markdown(
            f'<div class="kb-status kb-ready">'
            f'<span class="icon">✅</span>'
            f'<span class="text"><strong>Good to go!</strong> We have reports for <strong>{ticker}</strong> saved in our database — the AI can use them during research.</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="kb-status kb-missing">'
            f'<span class="icon">⚠️</span>'
            f'<span class="text"><strong>We don\'t have {ticker} files yet</strong> — upload a report below, or just run analysis with live market data only.</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander(f"📥 Quick upload: Add a report for {ticker}", expanded=True):
            inline_file = st.file_uploader(
                f"Pick a report file (.txt or .pdf) for {ticker}",
                type=["txt", "pdf"],
                key=f"inline_uploader_{ticker}",
            )
            if inline_file is not None:
                if st.button(f"📥 Save {inline_file.name} for {ticker}", key=f"btn_index_{ticker}", use_container_width=True):
                    with st.spinner(f"Reading and saving {inline_file.name}..."):
                        try:
                            text = extract_text(inline_file, inline_file.name)
                            chunks = ingest_document_text(text, inline_file.name, ticker)
                            if chunks > 0:
                                st.success(f"Saved {chunks} text chunks for {ticker}! 🎉")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("Couldn't read text from that file — is it a scanned image?")
                        except Exception as e:
                            st.error(f"Something went wrong: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Price chart section
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Market Price Action</h3>
    </div>
    """, unsafe_allow_html=True)

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
        st.caption(f"No price history found for {ticker}.")

    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 1rem; font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
        <span style="font-weight: 600; color: #38bdf8;">LangGraph Pipeline:</span>
        <code>START</code> <span>➔</span>
        <span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Node: market_research</span>
        <span>➔</span>
        <span style="background: rgba(168, 85, 247, 0.12); color: #c084fc; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Node: trend_analysis</span>
        <span>➔</span>
        <code>END</code>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Run AI Research on This Stock", type="primary", use_container_width=True):
        workflow = WorkflowService()
        state = {"ticker": ticker}

        status_box = st.status(f"⚡ Running LangGraph workflow for **{ticker}**...", expanded=True)
        with status_box:
            st.write("📍 **Edge 1:** Traversing `START` ➔ `market_research` node...")
            for step in workflow.stream({"ticker": ticker}):
                for node_name, updated_state in step.items():
                    state.update(updated_state)
                    if node_name == "market_research":
                        st.write("✅ **Node 1 Complete:** `market_research` (10-K RAG fundamentals extracted)")
                        st.write("📍 **Edge 2:** Traversing `market_research` ➔ `trend_analysis` node...")
                    elif node_name == "trend_analysis":
                        st.write("✅ **Node 2 Complete:** `trend_analysis` (market sentiment & sector trends analyzed)")
                        st.write("🏁 **Edge 3:** Traversing `trend_analysis` ➔ `END`")
            status_box.update(label=f"✅ LangGraph workflow complete for {ticker}!", state="complete", expanded=False)

        st.success(f"Done! Here's what we found for **{ticker}**")

        # display fundamental metrics
        fundamentals = state.get("fundamentals", {})
        metrics = fundamentals.get("metrics", {})
        summary = fundamentals.get("summary", "")
        risks = state.get("risks", [])

        if metrics:
            st.markdown("""
            <div class="section-heading">
                <div class="accent-bar"></div>
                <h3>Key Financial Metrics</h3>
            </div>
            """, unsafe_allow_html=True)
            m_cols = st.columns(len(metrics))
            for col, (k, v) in zip(m_cols, metrics.items()):
                label = k.replace("_", " ").title()
                col.metric(label, v)

        if summary:
            st.markdown("""
            <div class="section-heading">
                <div class="accent-bar"></div>
                <h3>Performance Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(summary)

        # display market sentiment & sector trends
        sentiment = state.get("sentiment", {})
        if sentiment:
            st.markdown("""
            <div class="section-heading">
                <div class="accent-bar"></div>
                <h3>Market Sentiment & Sector Trends</h3>
            </div>
            """, unsafe_allow_html=True)

            s_col1, s_col2 = st.columns(2)
            sentiment_label = sentiment.get("label", "Neutral")
            if sentiment_label == "Bullish":
                label_icon, pill_class = "🟢", "pill-green"
            elif sentiment_label == "Bearish":
                label_icon, pill_class = "🔴", "pill-amber"
            else:
                label_icon, pill_class = "🟡", "pill-blue"

            with s_col1:
                st.metric("Sentiment", f"{label_icon} {sentiment_label}")
            with s_col2:
                score = sentiment.get("score", 0.0)
                st.metric("Confidence Score", f"{score:+.2f}")

            # sentiment confidence bar
            bar_pct = int((score + 1) / 2 * 100)
            bar_color = "#10b981" if score > 0.2 else ("#f59e0b" if score > -0.2 else "#ef4444")
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.05); border-radius:8px; height:8px; margin:8px 0 16px; overflow:hidden;">'
                f'<div style="width:{bar_pct}%; height:100%; background:{bar_color}; border-radius:8px; transition: width 0.5s;"></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if sentiment.get("summary"):
                st.write(sentiment.get("summary"))

            col_tail, col_risk = st.columns(2)
            with col_tail:
                tailwinds = sentiment.get("sector_tailwinds", [])
                if tailwinds:
                    st.markdown("**🟢 Sector Catalysts & Tailwinds**")
                    for item in tailwinds:
                        st.markdown(f"- {item}")
            with col_risk:
                macro_risks = sentiment.get("macro_risks", [])
                if macro_risks:
                    st.markdown("**🔴 Macro & Regulatory Headwinds**")
                    for item in macro_risks:
                        st.markdown(f"- {item}")

        # display filing risk factors
        if risks:
            st.markdown("""
            <div class="section-heading">
                <div class="accent-bar"></div>
                <h3>SEC Filing Risk Factors</h3>
            </div>
            """, unsafe_allow_html=True)
            for r in risks:
                st.markdown(f"- {r}")


# ═══════════════════════════════════════════════════════
# TAB 3 — Analyst Review (HITL)
# ═══════════════════════════════════════════════════════
with tab_review:
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Review AI Results</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="kb-status kb-ready">'
        '<span class="icon">📋</span>'
        '<span class="text">Nothing to review yet! Go to the <strong>🔬 Run Analysis</strong> tab first to generate a research report.</span>'
        '</div>',
        unsafe_allow_html=True,
    )
