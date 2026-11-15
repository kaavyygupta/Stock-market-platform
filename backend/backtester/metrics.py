from data import load_prices
from engine import run_backtest
from portfolio import Portfolio


def total_return(values):
    return (values.iloc[-1] / values.iloc[0] - 1) * 100


def max_drawdown(values):
    # cummax() gives the highest value seen so far on each day.
    highest_so_far = values.cummax()
    drops = (values / highest_so_far - 1) * 100
    return drops.min()


def buy_and_hold_values(prices, starting_cash):
    account = Portfolio(starting_cash)
    account.buy(prices["Close"].iloc[0])
    return account.cash + account.shares * prices["Close"]


def print_report(ticker, starting_cash=10000, days=20):
    prices = load_prices(ticker)
    strategy = run_backtest(ticker, starting_cash, days)
    holding = buy_and_hold_values(prices, starting_cash)

    print(f"=== {ticker} ({days}-day average) ===")
    print(f"{'':15}{'Strategy':>12}{'Buy & hold':>14}")
    print(f"{'Final value':15}{strategy.iloc[-1]:>12,.0f}{holding.iloc[-1]:>14,.0f}")
    print(f"{'Total return':15}{total_return(strategy):>11.1f}%{total_return(holding):>13.1f}%")
    print(f"{'Biggest drop':15}{max_drawdown(strategy):>11.1f}%{max_drawdown(holding):>13.1f}%")
    print()


if __name__ == "__main__":
    for ticker in ["AAPL", "MSFT", "JPM", "XOM", "KO"]:
        print_report(ticker)
