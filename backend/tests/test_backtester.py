import pandas as pd

import engine
from data import load_prices
from portfolio import Portfolio
from strategy import stock_decider


def make_prices(closes):
    return pd.DataFrame({"Close": closes})


def test_load_prices_is_sorted_oldest_first():
    prices = load_prices("AAPL")
    assert len(prices) > 0
    assert prices.index.is_monotonic_increasing


def test_portfolio_buy_and_sell():
    account = Portfolio(10000)
    account.buy(150)
    assert account.shares == 66
    assert account.cash == 100
    assert account.total_value(160) == 10660

    account.sell(160)
    assert account.shares == 0
    assert account.cash == 10660


def test_portfolio_ignores_repeat_buys_and_empty_sells():
    account = Portfolio(10000)
    account.sell(150)
    assert account.cash == 10000

    account.buy(150)
    account.buy(10)
    assert account.shares == 66


def test_strategy_holds_without_enough_data():
    assert stock_decider(make_prices([100] * 10)) == "hold"


def test_strategy_buys_in_uptrend():
    assert stock_decider(make_prices(list(range(100, 120)))) == "buy"


def test_strategy_sells_in_downtrend():
    assert stock_decider(make_prices(list(range(120, 100, -1)))) == "sell"


def test_engine_never_uses_future_prices(monkeypatch):
    normal = engine.run_backtest("AAPL")

    changed = load_prices("AAPL")
    changed.loc[changed.index[500:], "Close"] = 1.0
    monkeypatch.setattr(engine, "load_prices", lambda ticker: changed)
    with_future_changed = engine.run_backtest("AAPL")

    assert normal.iloc[:500].equals(with_future_changed.iloc[:500])
    assert not normal.iloc[500:].equals(with_future_changed.iloc[500:])
