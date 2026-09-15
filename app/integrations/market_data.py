import yfinance as yf
import pandas as pd


def fetch_ticker_fundamentals(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    return {
        "info": t.info,
        "calendar": t.calendar,
        "financials": t.financials.to_dict() if not t.financials.empty else {},
    }


def fetch_stock_overview(ticker: str) -> dict:
    """Fetch real-time snapshot metrics (price, daily change, 52-week range)."""
    try:
        t = yf.Ticker(ticker)
        fast = t.fast_info
        current = getattr(fast, "last_price", None)
        prev_close = getattr(fast, "previous_close", None)
        currency = getattr(fast, "currency", "USD")

        change = (current - prev_close) if (current is not None and prev_close is not None) else 0.0
        change_pct = (change / prev_close * 100) if (prev_close and prev_close > 0) else 0.0

        return {
            "current_price": current,
            "prev_close": prev_close,
            "change": change,
            "change_pct": change_pct,
            "currency": currency,
            "fifty_two_week_high": getattr(fast, "year_high", None),
            "fifty_two_week_low": getattr(fast, "year_low", None),
        }
    except Exception as e:
        print("couldnt get overview for", ticker, e)
        return {}


def fetch_price_history(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """Fetch historical daily close prices for charting."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        if hist.empty:
            return pd.DataFrame()
        # Remove timezone offset for clean Streamlit line_chart display
        if hist.index.tz is not None:
            hist.index = hist.index.tz_localize(None)
        return hist[["Close"]]
    except Exception as e:
        print("couldnt get history for", ticker, e)
        return pd.DataFrame()


def fetch_valuation_metrics(ticker: str) -> dict:
    """Fetch key valuation multiples and market metrics for comparative analysis."""
    try:
        t = yf.Ticker(ticker)
        fast = t.fast_info
        info = {}
        try:
            info = t.info or {}
        except Exception:
            info = {}

        price = getattr(fast, "last_price", None) or info.get("currentPrice") or info.get("regularMarketPrice")
        mcap = getattr(fast, "market_cap", None) or info.get("marketCap")
        pe = info.get("trailingPE")
        fwd_pe = info.get("forwardPE")
        high = getattr(fast, "year_high", None) or info.get("fiftyTwoWeekHigh")
        low = getattr(fast, "year_low", None) or info.get("fiftyTwoWeekLow")
        name = info.get("shortName") or info.get("longName") or ticker
        currency = getattr(fast, "currency", "USD") or info.get("currency", "USD")

        def fmt_mcap(val):
            if not val:
                return "N/A"
            if val >= 1e12:
                return f"${val / 1e12:.2f}T"
            if val >= 1e9:
                return f"${val / 1e9:.2f}B"
            if val >= 1e6:
                return f"${val / 1e6:.2f}M"
            return f"${val:,.0f}"

        return {
            "ticker": ticker.upper(),
            "name": name,
            "current_price": f"${price:.2f}" if price else "N/A",
            "market_cap": fmt_mcap(mcap),
            "pe_ratio": f"{pe:.1f}x" if pe else "N/A",
            "forward_pe": f"{fwd_pe:.1f}x" if fwd_pe else "N/A",
            "fifty_two_week_high": f"${high:.2f}" if high else "N/A",
            "fifty_two_week_low": f"${low:.2f}" if low else "N/A",
            "currency": currency,
        }
    except Exception as e:
        print("valuation fetch failed for", ticker, e)
        return {
            "ticker": ticker.upper(),
            "name": ticker.upper(),
            "current_price": "N/A",
            "market_cap": "N/A",
            "pe_ratio": "N/A",
            "forward_pe": "N/A",
            "fifty_two_week_high": "N/A",
            "fifty_two_week_low": "N/A",
            "currency": "USD",
        }

