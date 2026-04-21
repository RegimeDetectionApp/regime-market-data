"""
Data loading utilities for market regime detection.

Fetches OHLCV data from Yahoo Finance for supported asset classes.
"""

import time
import yfinance as yf
import pandas as pd

# Supported tickers with human-readable names
ASSET_UNIVERSE = {
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ Composite",
    "^NSEI": "NIFTY 50",
    "GC=F": "Gold Futures",
}


def fetch_data(
    ticker: str,
    start: str = "2005-01-01",
    end: str | None = None,
) -> pd.DataFrame:
    """
    Download daily OHLCV data for a single ticker.

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker symbol (e.g. "^GSPC").
    start : str
        Start date in YYYY-MM-DD format.
    end : str or None
        End date. Defaults to today.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by Date with columns
        [Open, High, Low, Close, Adj Close, Volume].
    """
    # Retry up to 3 times to handle transient Yahoo Finance errors
    for attempt in range(3):
        try:
            df = yf.download(ticker, start=start, end=end, progress=False)
            if len(df) > 0:
                break
        except Exception:
            df = pd.DataFrame()
        if attempt < 2:
            time.sleep(2)

    if len(df) == 0:
        raise RuntimeError(
            f"No data returned for {ticker}. Check the ticker symbol "
            f"and your internet connection."
        )

    # yfinance may return MultiIndex columns for single ticker; flatten
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    # Drop rows where Close is missing (market holidays / gaps)
    df.dropna(subset=["Close"], inplace=True)

    return df


def get_asset_name(ticker: str) -> str:
    """Return human-readable name for a ticker, or the ticker itself."""
    return ASSET_UNIVERSE.get(ticker, ticker)
