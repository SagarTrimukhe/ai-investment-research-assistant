import yfinance as yf


def fetch_ticker_fundamentals(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    return {
        "info": t.info,
        "calendar": t.calendar,
        "financials": t.financials.to_dict() if not t.financials.empty else {},
    }
