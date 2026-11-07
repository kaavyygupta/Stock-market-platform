class Portfolio:
    def __init__(self, starting_cash):
        self.cash = starting_cash
        self.shares = 0

    def buy(self, price):
        if self.shares > 0:
            return

        shares_to_buy = int(self.cash // price)
        self.shares = self.shares + shares_to_buy
        self.cash = self.cash - shares_to_buy * price

    def sell(self, price):
        if self.shares == 0:
            return

        self.cash = self.cash + self.shares * price
        self.shares = 0

    def total_value(self, price):
        return self.cash + self.shares * price


if __name__ == "__main__":
    account = Portfolio(10000)
    print("Start:", account.cash, account.shares)

    account.buy(150)
    print("After buy:", account.cash, account.shares)
    print("Value at 160:", account.total_value(160))

    account.sell(160)
    print("After sell:", account.cash, account.shares)
