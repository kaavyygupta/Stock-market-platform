import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException

# The backtester files import each other by plain name (e.g. "from data import ..."),
# so Python needs their folder on its search path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backtester"))

from data import load_prices
from engine import run_backtest
from metrics import buy_and_hold_values, max_drawdown, total_return

app = FastAPI(title="Stock Market Platform")


def summarize(values):
    return {
        "final_value": round(values.iloc[-1], 2),
        "total_return": round(total_return(values), 2),
        "max_drawdown": round(max_drawdown(values), 2),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/backtest/{ticker}")
def backtest(ticker: str, days: int = 20, starting_cash: float = 10000):
    ticker = ticker.upper()
    try:
        prices = load_prices(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No price data for {ticker}")

    strategy = run_backtest(ticker, starting_cash, days)
    holding = buy_and_hold_values(prices, starting_cash)

    return {
        "ticker": ticker,
        "days": days,
        "starting_cash": starting_cash,
        "strategy": summarize(strategy),
        "buy_and_hold": summarize(holding),
    }
