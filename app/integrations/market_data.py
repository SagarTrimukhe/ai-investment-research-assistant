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
