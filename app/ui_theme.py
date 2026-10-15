import streamlit as st


def inject_custom_css():
    """Injects high-end, institutional Sleek Slate Dark theme CSS (TradingView/Bloomberg Dark style)."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Verified Institutional Sleek Slate Dark Theme Tokens */
    :root {
        --primary-blue: #3B82F6;
        --primary-hover: #60A5FA;
        --primary-light: rgba(59, 130, 246, 0.15);
        --accent-cyan: #06B6D4;
        --accent-emerald: #10B981;
        --accent-amber: #F59E0B;
        --accent-rose: #F43F5E;
        
        --bg-canvas: #0B0F19;
        --bg-card: #151D2C;
        --bg-card-alt: #0F172A;
        
        --border-subtle: #222F44;
        --border-medium: #334155;
        --border-focus: #3B82F6;
        
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --text-light: #64748B;
        
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 8px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 12px 24px -4px rgba(0, 0, 0, 0.5);
    }

    .stApp {
        background-color: var(--bg-canvas) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #0D131F !important;
        border-right: 1px solid var(--border-subtle) !important;
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="stSidebarUserContent"] {
        padding-top: 1.25rem !important;
    }

    /* Tabs Bar */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 6px !important;
        background: #0F172A !important;
        padding: 5px 6px !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-subtle) !important;
        margin-bottom: 22px !important;
    }

    [data-testid="stTabs"] [role="tab"] {
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        color: var(--text-muted) !important;
        padding: 9px 20px !important;
        transition: all 0.2s ease !important;
        border: none !important;
        background: transparent !important;
    }

    [data-testid="stTabs"] [role="tab"]:hover {
        color: var(--text-primary) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: #1E293B !important;
        color: #60A5FA !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid var(--border-medium) !important;
    }

    [data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #151D2C !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.25s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }

    [data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-blue), #06B6D4);
        opacity: 0.9;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: var(--border-medium) !important;
        box-shadow: var(--shadow-md) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: var(--text-muted) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: #151D2C !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        margin-bottom: 14px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"]:hover {
        border-color: var(--border-medium) !important;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        color: var(--text-primary) !important;
        padding: 12px 18px !important;
    }

    /* Buttons */
    .stButton > button[kind="primary"], button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 24px !important;
        box-shadow: 0 2px 10px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="primary"]:hover, button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.45) !important;
        background: #1D4ED8 !important;
    }

    .stButton > button[kind="secondary"], button[data-testid="baseButton-secondary"] {
        background: #151D2C !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="secondary"]:hover, button[data-testid="baseButton-secondary"]:hover {
        background: #1E293B !important;
        border-color: var(--primary-blue) !important;
        color: #60A5FA !important;
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: #151D2C !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.92rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #151D2C !important;
        border: 2px dashed var(--border-medium) !important;
        border-radius: 14px !important;
        padding: 18px !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-blue) !important;
        background: #1E293B !important;
    }

    /* Alerts */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid var(--border-subtle) !important;
        box-shadow: var(--shadow-sm) !important;
        background-color: #151D2C !important;
    }

    /* Ticker Tape Animation */
    @keyframes marquee {
        0% { transform: translateX(0%); }
        100% { transform: translateX(-50%); }
    }

    .ticker-tape-container {
        overflow: hidden;
        white-space: nowrap;
        background: #151D2C;
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 8px 0;
        margin-bottom: 20px;
        box-shadow: var(--shadow-sm);
    }

    .ticker-tape-content {
        display: inline-block;
        white-space: nowrap;
        animation: marquee 45s linear infinite;
    }

    .ticker-tape-container:hover .ticker-tape-content {
        animation-play-state: paused;
    }

    .ticker-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin: 0 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: var(--text-secondary);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        vertical-align: middle;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
    }

    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
    </style>
    """
    st.html(css)


def render_hero_banner():
    """Renders an executive, Sleek Slate Dark institutional banner."""
    html = """
    <div style="
        background: #151D2C;
        border: 1px solid #222F44;
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 22px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3B82F6, #06B6D4, #10B981);
        "></div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 0.70rem;
                        font-weight: 700;
                        letter-spacing: 0.08em;
                        color: #60A5FA;
                        background: rgba(59, 130, 246, 0.15);
                        padding: 3px 9px;
                        border-radius: 6px;
                        border: 1px solid rgba(59, 130, 246, 0.35);
                        text-transform: uppercase;
                    ">✦ AUTONOMOUS EQUITY INTELLIGENCE</span>
                    <span style="
                        font-size: 0.70rem;
                        font-weight: 600;
                        color: #94A3B8;
                        background: #1E293B;
                        padding: 3px 9px;
                        border-radius: 6px;
                        border: 1px solid #334155;
                    ">LANGGRAPH v0.2 · GEMINI 2.5 FLASH</span>
                </div>
                <h1 style="
                    margin: 0;
                    font-size: 2.1rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                    color: #F8FAFC;
                ">AI Investment Research Assistant</h1>
                <p style="
                    margin: 5px 0 0 0;
                    color: #94A3B8;
                    font-size: 0.94rem;
                    font-weight: 400;
                    max-width: 720px;
                ">Autonomous multi-agent equity research platform executing 10-K extraction, peer comparative valuation, macroeconomic sentiment, and certified investment theses.</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">
                <div style="
                    display: inline-flex;
                    align-items: center;
                    background: rgba(16, 185, 129, 0.15);
                    border: 1px solid rgba(16, 185, 129, 0.35);
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.76rem;
                    font-weight: 600;
                    color: #34D399;
                ">
                    <span class="pulse-dot"></span> SEC EDGAR & ChromaDB Online
                </div>
                <span style="font-size: 0.74rem; color: #94A3B8;">Autonomous Equity Intelligence Platform</span>
            </div>
        </div>
    </div>
    """
    st.html(html)


def render_sidebar_branding():
    """Renders the top sidebar card with logo and project metadata."""
    html = """
    <div style="
        background: #151D2C;
        border: 1px solid #222F44;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 18px;
    ">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <div style="
                width: 36px;
                height: 36px;
                border-radius: 8px;
                background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.15rem;
                color: #FFFFFF;
                box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
            ">📊</div>
            <div>
                <div style="font-weight: 700; font-size: 1rem; color: #F8FAFC; letter-spacing: -0.01em;">Research Assistant</div>
                <div style="font-size: 0.74rem; color: #60A5FA; font-weight: 600;">Multi-Agent Equity Suite</div>
            </div>
        </div>
        <div style="font-size: 0.74rem; color: #94A3B8; border-top: 1px solid #222F44; padding-top: 8px; margin-top: 6px;">
            Autonomous Equity Intelligence Platform
        </div>
    </div>
    """
    st.sidebar.html(html)


def render_sidebar_system_info(s3_status: bool):
    """Renders clean styled badges for system services in Sleek Slate Dark mode."""
    storage_label = "AWS S3 Active" if s3_status else "Local + S3 Ready"
    storage_color = "#34D399" if s3_status else "#38BDF8"
    storage_bg = "rgba(16, 185, 129, 0.15)" if s3_status else "rgba(56, 189, 248, 0.15)"
    storage_border = "rgba(16, 185, 129, 0.35)" if s3_status else "rgba(56, 189, 248, 0.35)"

    html = f"""
    <div style="margin-bottom: 18px;">
        <div style="
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94A3B8;
            font-weight: 700;
            margin-bottom: 8px;
        ">Active Infrastructure</div>
        
        <div style="display: flex; flex-direction: column; gap: 6px;">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #151D2C;
                padding: 6px 11px;
                border-radius: 8px;
                border: 1px solid #222F44;
            ">
                <span style="font-size: 0.78rem; color: #CBD5E1;">LLM Engine</span>
                <span style="
                    font-size: 0.70rem;
                    font-family: 'JetBrains Mono', monospace;
                    font-weight: 600;
                    color: #C084FC;
                    background: rgba(168, 85, 247, 0.15);
                    padding: 2px 7px;
                    border-radius: 5px;
                    border: 1px solid rgba(168, 85, 247, 0.35);
                ">Gemini 2.5 Flash</span>
            </div>

            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #151D2C;
                padding: 6px 11px;
                border-radius: 8px;
                border: 1px solid #222F44;
            ">
                <span style="font-size: 0.78rem; color: #CBD5E1;">Vector DB</span>
                <span style="
                    font-size: 0.70rem;
                    font-family: 'JetBrains Mono', monospace;
                    font-weight: 600;
                    color: #38BDF8;
                    background: rgba(56, 189, 248, 0.15);
                    padding: 2px 7px;
                    border-radius: 5px;
                    border: 1px solid rgba(56, 189, 248, 0.35);
                ">ChromaDB</span>
            </div>

            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #151D2C;
                padding: 6px 11px;
                border-radius: 8px;
                border: 1px solid #222F44;
            ">
                <span style="font-size: 0.78rem; color: #CBD5E1;">Storage</span>
                <span style="
                    font-size: 0.70rem;
                    font-family: 'JetBrains Mono', monospace;
                    font-weight: 600;
                    color: {storage_color};
                    background: {storage_bg};
                    padding: 2px 7px;
                    border-radius: 5px;
                    border: 1px solid {storage_border};
                ">{storage_label}</span>
            </div>
        </div>
    </div>
    """
    st.sidebar.html(html)


def render_sidebar_tickers(indexed_list):
    """Renders clean ticker pill tags in Sleek Slate Dark mode."""
    pills = "".join([
        f'<span style="font-family:\'JetBrains Mono\',monospace; font-size:0.74rem; font-weight:700; '
        f'color:#34D399; background:rgba(16, 185, 129, 0.15); border:1px solid rgba(16, 185, 129, 0.35); '
        f'padding:2px 8px; border-radius:5px; display:inline-block; margin:2px;">{t}</span>'
        for t in indexed_list
    ]) if indexed_list else '<span style="color:#64748B; font-size:0.78rem;">No filings indexed yet.</span>'

    html = f"""
    <div style="margin-top: 12px; margin-bottom: 6px;">
        <div style="
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94A3B8;
            font-weight: 700;
            margin-bottom: 6px;
        ">Indexed Filings ({len(indexed_list)})</div>
        <div style="display:flex; flex-wrap:wrap; gap:3px; margin-bottom:14px;">
            {pills}
        </div>
    </div>
    """
    st.sidebar.html(html)


def render_sidebar_footer():
    """Renders clean styled footer in the sidebar."""
    html = """
    <div style="
        font-size: 0.70rem;
        color: #64748B;
        border-top: 1px solid #222F44;
        padding-top: 14px;
        margin-top: 20px;
        text-align: center;
    ">
        Autonomous Equity Intelligence · Enterprise Platform
    </div>
    """
    st.sidebar.html(html)


def render_section_title(title: str, subtitle: str = "", icon: str = ""):
    """Renders a styled section title with an accent bar in Sleek Slate Dark mode."""
    icon_html = f'<span style="margin-right: 8px; font-size: 1.15rem;">{icon}</span>' if icon else ""
    sub_html = f'<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 3px;">{subtitle}</div>' if subtitle else ""
    html = f"""
    <div style="margin-top: 18px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center;">
            <div style="
                width: 3px;
                height: 20px;
                background: #3B82F6;
                border-radius: 2px;
                margin-right: 10px;
            "></div>
            <h3 style="
                margin: 0;
                font-size: 1.25rem;
                font-weight: 700;
                letter-spacing: -0.01em;
                color: #F8FAFC;
                display: flex;
                align-items: center;
            ">{icon_html}{title}</h3>
        </div>
        {sub_html}
    </div>
    """
    st.html(html)


def render_glass_card(title: str, items: list, icon: str = "📌", accent_color: str = "#3B82F6"):
    """Renders a sleek slate card container with structured bullet points."""
    items_html = "".join([f'<li style="margin-bottom: 6px; color: #CBD5E1; line-height: 1.5;">{item}</li>' for item in items])
    card_html = f"""
    <div style="
        background: #151D2C;
        border: 1px solid #222F44;
        border-top: 3px solid {accent_color};
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 7px;
            font-size: 0.92rem;
            font-weight: 700;
            color: #F8FAFC;
            margin-bottom: 10px;
        ">
            <span>{icon}</span>
            <span>{title}</span>
        </div>
        <ul style="margin: 0; padding-left: 18px; font-size: 0.86rem;">
            {items_html}
        </ul>
    </div>
    """
    st.html(card_html)


def render_executive_summary(exec_sum: str):
    """Renders an executive summary callout in Sleek Slate Dark mode."""
    html = f"""
    <div style="
        background: rgba(59, 130, 246, 0.10);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-left: 3px solid #3B82F6;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 12px 0 18px 0;
        color: #E2E8F0;
        font-size: 0.92rem;
        line-height: 1.6;
    ">
        <strong style="color: #60A5FA; font-size: 0.95rem;">Executive Summary:</strong><br/>
        {exec_sum}
    </div>
    """
    st.html(html)


def render_ticker_tape():
    """Renders a clean horizontal market ticker tape in Sleek Slate Dark mode."""
    sample_tickers = [
        {"ticker": "AAPL", "price": "$232.15", "change": "+1.42%", "up": True},
        {"ticker": "NVDA", "price": "$138.07", "change": "+3.13%", "up": True},
        {"ticker": "MSFT", "price": "$420.55", "change": "-0.38%", "up": False},
        {"ticker": "META", "price": "$588.62", "change": "+2.24%", "up": True},
        {"ticker": "AMZN", "price": "$187.97", "change": "+0.85%", "up": True},
        {"ticker": "GOOGL", "price": "$166.12", "change": "-0.22%", "up": False},
        {"ticker": "TSLA", "price": "$221.86", "change": "+4.12%", "up": True},
    ]

    items_html = ""
    for item in sample_tickers * 2:
        color = "#10B981" if item["up"] else "#F43F5E"
        arrow = "▲" if item["up"] else "▼"
        items_html += f"""
        <span class="ticker-item">
            <strong style="color: #F8FAFC;">{item['ticker']}</strong>
            <span style="color: #94A3B8;">{item['price']}</span>
            <span style="color: {color}; font-weight: 600;">{arrow} {item['change']}</span>
        </span>
        <span style="color: #334155; margin: 0 4px;">•</span>
        """

    tape_html = f"""
    <div class="ticker-tape-container">
        <div class="ticker-tape-content">
            {items_html}
        </div>
    </div>
    """
    st.html(tape_html)


def render_52w_range_bar(current_price: float, low: float, high: float):
    """Renders a visual 52-week price range meter in Sleek Slate Dark mode."""
    if not (current_price and low and high and high > low):
        return

    pct = max(0.0, min(100.0, ((current_price - low) / (high - low)) * 100))

    html = f"""
    <div style="
        background: #151D2C;
        border: 1px solid #222F44;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 14px 0 18px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.07em; color: #94A3B8; font-weight: 700;">
                52-Week Range Position
            </span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; color: #60A5FA;">
                {pct:.1f}% of Range
            </span>
        </div>
        <div style="
            position: relative;
            background: #1E293B;
            height: 8px;
            border-radius: 4px;
            overflow: visible;
            margin: 8px 0 14px 0;
        ">
            <div style="
                width: {pct:.1f}%;
                height: 100%;
                background: linear-gradient(90deg, #10B981 0%, #3B82F6 100%);
                border-radius: 4px;
                transition: width 0.8s ease;
            "></div>
            <div style="
                position: absolute;
                left: calc({pct:.1f}% - 6px);
                top: -3px;
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: #151D2C;
                border: 2px solid #3B82F6;
                box-shadow: 0 0 6px rgba(59, 130, 246, 0.5);
            "></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #94A3B8;">
            <span>52W Low: <strong style="color: #F43F5E;">${low:.2f}</strong></span>
            <span>Current: <strong style="color: #F8FAFC;">${current_price:.2f}</strong></span>
            <span>52W High: <strong style="color: #10B981;">${high:.2f}</strong></span>
        </div>
    </div>
    """
    st.html(html)


def render_agent_stepper_visualizer(completed_nodes: list = None):
    """Renders a visual stepper showing the active multi-agent pipeline in Sleek Slate Dark mode."""
    nodes = [
        ("Router", "🎯", "router"),
        ("10-K Retrieval", "📂", "market_research"),
        ("Market Trends", "🌐", "trend_analysis"),
        ("Peer Valuation", "⚖️", "comparative_analysis"),
        ("Thesis Synthesis", "💡", "summary_agent"),
        ("HITL Review Gate", "🛡️", "review"),
    ]

    completed_nodes = completed_nodes or []
    stepper_html = '<div style="display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 18px;">'

    for name, icon, key in nodes:
        is_done = key in completed_nodes
        is_active = (not is_done) and (len(completed_nodes) == [k for _, _, k in nodes].index(key))
        bg = "rgba(16, 185, 129, 0.15)" if is_done else ("rgba(59, 130, 246, 0.15)" if is_active else "#151D2C")
        border = "rgba(16, 185, 129, 0.35)" if is_done else ("rgba(59, 130, 246, 0.35)" if is_active else "#222F44")
        color = "#34D399" if is_done else ("#60A5FA" if is_active else "#94A3B8")

        stepper_html += f"""
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: {bg};
            border: 1px solid {border};
            padding: 5px 11px;
            border-radius: 7px;
            font-size: 0.76rem;
            font-weight: 600;
            color: {color};
        ">
            <span>{icon}</span>
            <span>{name}</span>
            {'<span style="color:#10B981; margin-left:2px;">✓</span>' if is_done else ''}
        </div>
        """
    stepper_html += '</div>'
    st.html(stepper_html)
