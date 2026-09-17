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
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-size: 2.5rem;">📊</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #e2e8f0; margin-top: 0.3rem;">
            Research Control Center
        </div>
        <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 0.2rem;">
            Multi-Agent Equity Research Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # System info cards
    st.markdown("""
    <div class="info-card">
        <h4>🤖 Language Model</h4>
        <div class="value">Gemini 1.5 Flash</div>
        <div style="margin-top:4px;">
            <span class="status-pill pill-green">● Online</span>
            <span style="color:#94a3b8; font-size:0.78rem; margin-left:8px;">temp: 0.1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>🗄️ Vector Database</h4>
        <div class="value">ChromaDB</div>
        <div style="margin-top:4px;">
            <span class="status-pill pill-blue">financial_filings</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Indexed companies
    indexed_list = get_indexed_tickers()
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Indexed Companies</h3>
    </div>
    """, unsafe_allow_html=True)

    if indexed_list:
        chips_html = "".join(
            f'<span class="ticker-chip">📄 {t}</span>' for t in indexed_list
        )
        st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:4px;">{chips_html}</div>', unsafe_allow_html=True)
    else:
        st.caption("No filings indexed yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Theme 15 • Multi-Agent Research with HITL Review")


# ── Main content header ──
st.markdown("""
<div class="main-header">
    <h1>📊 AI Investment Research Assistant</h1>
    <p>Theme 15 — Multi-Agent Equity Research with Human-in-the-Loop Review</p>
</div>
""", unsafe_allow_html=True)

tab_ingest, tab_analysis, tab_review = st.tabs([
    "📁 Document Ingestion",
    "🔬 Research & Analysis",
    "✅ Analyst Review (HITL)",
])


# ═══════════════════════════════════════════════════════
# TAB 1 — Document Ingestion
# ═══════════════════════════════════════════════════════
with tab_ingest:
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Upload SEC Filings & Reports</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Index 10-K, 10-Q, or market research files into the ChromaDB vector store for RAG-powered analysis.")

    st.markdown("<br>", unsafe_allow_html=True)

    ingest_col1, ingest_col2 = st.columns([1, 2])
    with ingest_col1:
        ingest_ticker = st.text_input(
            "🏷️ Stock Ticker",
            value="AAPL",
            key="ingest_ticker_input",
            help="Enter the ticker symbol for the company whose filing you are uploading.",
        ).upper().strip()
    with ingest_col2:
        uploaded_files = st.file_uploader(
            f"📎 Drop filing documents for **{ingest_ticker}**",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            key="general_uploader",
        )

    if uploaded_files:
        st.markdown(
            f'<div class="kb-status kb-ready">'
            f'<span class="icon">📄</span>'
            f'<span class="text">Selected <strong>{len(uploaded_files)}</strong> document(s) for <strong>{ingest_ticker}</strong></span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(f"⚡ Process & Index to ChromaDB ({ingest_ticker})", type="primary", use_container_width=True):
            total_chunks = 0
            with st.spinner(f"Extracting, chunking, and embedding documents for {ingest_ticker}..."):
                for up_file in uploaded_files:
                    text = extract_text(up_file, up_file.name)
                    chunks = ingest_document_text(text, up_file.name, ingest_ticker)
                    total_chunks += chunks
            if total_chunks > 0:
                st.success(f"✅ Indexed **{total_chunks} chunks** into ChromaDB for **{ingest_ticker}**!")
                st.balloons()
                st.rerun()
            else:
                st.error("Could not extract readable text from the uploaded files.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Currently indexed stocks
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Knowledge Base Status</h3>
    </div>
    """, unsafe_allow_html=True)

    current_indexed = get_indexed_tickers()
    if current_indexed:
        chips_html = "".join(
            f'<span class="ticker-chip">📄 {t} — Indexed</span>' for t in current_indexed
        )
        st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">{chips_html}</div>', unsafe_allow_html=True)
    else:
        st.info("No filings currently indexed. Upload a 10-K or 10-Q filing above to get started.")


# ═══════════════════════════════════════════════════════
# TAB 2 — Research & Analysis
# ═══════════════════════════════════════════════════════
with tab_analysis:
    st.markdown("""
    <div class="section-heading">
        <div class="accent-bar"></div>
        <h3>Configure Analysis</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("🎯 Target Ticker", value="AAPL").upper().strip()
    with col2:
        benchmark = st.text_input("📊 Benchmark Ticker", value="MSFT").upper().strip()

    # Knowledge base check with styled banner
    is_indexed = is_ticker_indexed(ticker)
    if is_indexed:
        st.markdown(
            f'<div class="kb-status kb-ready">'
            f'<span class="icon">✅</span>'
            f'<span class="text"><strong>Knowledge Base Ready</strong> — SEC 10-K filings for <strong>{ticker}</strong> are indexed and available for RAG extraction.</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="kb-status kb-missing">'
            f'<span class="icon">⚠️</span>'
            f'<span class="text"><strong>{ticker} not in Knowledge Base</strong> — No SEC filings indexed. Upload a filing below, or proceed with public market data only.</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander(f"📥 Quick Index: Upload a filing for {ticker}", expanded=True):
            inline_file = st.file_uploader(
                f"Choose a 10-K / 10-Q filing (.txt or .pdf) for {ticker}",
                type=["txt", "pdf"],
                key=f"inline_uploader_{ticker}",
            )
            if inline_file is not None:
                if st.button(f"⚡ Index Filing for {ticker}", key=f"btn_index_{ticker}", use_container_width=True):
                    with st.spinner(f"Extracting and indexing {inline_file.name} for {ticker}..."):
                        text = extract_text(inline_file, inline_file.name)
                        chunks = ingest_document_text(text, inline_file.name, ticker)
                        if chunks > 0:
                            st.success(f"Indexed {chunks} chunks for {ticker}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Failed to parse text from the uploaded file.")

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

    st.markdown("---")

    if st.button("🚀 Start Research Workflow", type="primary", use_container_width=True):
        # step 1: market research (10-K RAG)
        with st.spinner(f"Agent 1/2 — Running market research for {ticker}..."):
            state = {"ticker": ticker}
            state = market_research_node(state)

        # step 2: trend and sentiment analysis
        with st.spinner(f"Agent 2/2 — Analyzing trends and sentiment for {ticker}..."):
            state = trend_analysis_node(state)

        st.success(f"✅ Analysis completed for **{ticker}**")

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
        <h3>Human-in-the-Loop Review Queue</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="kb-status kb-ready">'
        '<span class="icon">📋</span>'
        '<span class="text">No reports currently waiting for analyst review. Run a research workflow to generate a draft memo.</span>'
        '</div>',
        unsafe_allow_html=True,
    )
