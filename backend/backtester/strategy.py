from data import load_prices

#This function checks whether we need to hold, buy or sell the stock
#by checking the today's price and the average price of the last 20 days.
def stock_decider(prices_till_today, days=20):
    if len(prices_till_today) < days:
        return "hold"

    todays_price = prices_till_today["Close"].iloc[-1]

    average_price = prices_till_today["Close"].tail(days).mean()

    if todays_price > average_price:
        return "buy"
    elif todays_price < average_price:
        return "sell"
    else:
        return "hold"

if __name__ == "__main__":
    prices = load_prices("AAPL")
    print(stock_decider(prices.head(10)))
    print(stock_decider(prices.head(100)))

