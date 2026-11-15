import pandas as pd

from data import load_prices
from strategy import stock_decider
from portfolio import Portfolio


def run_backtest(ticker, starting_cash=10000, days=20):
    """Replay one stock's price history day by day and return the account value for each day."""
    prices = load_prices(ticker)
    account = Portfolio(starting_cash)
    daily_values = []

    for i in range(len(prices)):
        # Only the rows up to and including today, so the strategy can't see the future.
        prices_till_today = prices.iloc[: i + 1]
        todays_price = prices_till_today["Close"].iloc[-1]

        signal = stock_decider(prices_till_today, days)
        if signal == "buy":
            account.buy(todays_price)
        elif signal == "sell":
            account.sell(todays_price)

        daily_values.append(account.total_value(todays_price))

    # Label each value with its date, so later steps know which day it belongs to.
    return pd.Series(daily_values, index=prices.index)


if __name__ == "__main__":
    values = run_backtest("AAPL")
    print(values.head())
    print(values.tail())
    print("Started with:", values.iloc[0])
    print("Ended with:", round(values.iloc[-1], 2))
