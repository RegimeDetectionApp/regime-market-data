# regime-market-data

Market data acquisition anti-corruption layer for the regime detection system.

## Bounded Context

Fetches and normalizes OHLCV market data from Yahoo Finance. Provides a clean DataFrame interface decoupled from the data source.

## Installation

```bash
pip install git+https://github.com/govid13427742/regime-market-data.git@main
```

## API

| Function | Description |
|----------|-------------|
| `fetch_data(ticker, start, end)` | Download daily OHLCV data with retry logic |
| `get_asset_name(ticker)` | Human-readable name for a ticker |
| `ASSET_UNIVERSE` | Dict of supported tickers and names |

## Output Contract

`fetch_data()` returns a `pd.DataFrame`:
- **Index**: `pd.DatetimeIndex` (sorted ascending)
- **Columns**: `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`
- **Guarantees**: No NaN in `Close`, sorted by date

## Dependencies

- yfinance, pandas
