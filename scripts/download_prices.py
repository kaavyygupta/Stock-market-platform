"""Download daily historical prices and save one CSV per stock into data/.

Run once from the project folder:
    python scripts/download_prices.py
"""

from pathlib import Path

import yfinance as yf

# A mix of companies from different industries, so the backtester
# gets tested on different kinds of price movement.
TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "KO"]

# How much history to download ("5y" = the last 5 years).
PERIOD = "5y"

# Save into the data/ folder next to scripts/, no matter where we run from.
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)  # create data/ if it doesn't exist yet

for ticker in TICKERS:
    # One row per trading day: Open, High, Low, Close, Volume (+ extras).
    # Prices are adjusted for stock splits and dividends by default,
    # so a split doesn't look like a sudden crash.
    prices = yf.Ticker(ticker).history(period=PERIOD)

    # Keep only the columns the backtester needs.
    prices = prices[["Open", "High", "Low", "Close", "Volume"]]

    # Dates come with a time and timezone (e.g. "2021-10-20 00:00:00-04:00").
    # Daily bars only need the date part.
    prices.index = prices.index.date
    prices.index.name = "Date"

    output_file = DATA_DIR / f"{ticker}.csv"
    prices.to_csv(output_file)
    print(f"Saved {len(prices)} days of {ticker} to {output_file}")
