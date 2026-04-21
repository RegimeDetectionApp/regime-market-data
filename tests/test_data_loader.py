"""Tests for regime_market_data.data_loader."""

import pandas as pd
from regime_market_data import fetch_data, get_asset_name, ASSET_UNIVERSE


def test_asset_universe_contains_expected_tickers():
    assert "^GSPC" in ASSET_UNIVERSE
    assert "^IXIC" in ASSET_UNIVERSE
    assert "GC=F" in ASSET_UNIVERSE


def test_get_asset_name_known():
    assert get_asset_name("^GSPC") == "S&P 500"
    assert get_asset_name("^IXIC") == "NASDAQ Composite"


def test_get_asset_name_unknown_returns_ticker():
    assert get_asset_name("UNKNOWN") == "UNKNOWN"


def test_fetch_data_returns_dataframe():
    df = fetch_data("^GSPC", start="2024-01-01", end="2024-01-31")
    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert len(df) > 0
