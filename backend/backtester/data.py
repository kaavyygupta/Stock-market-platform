import pandas as pd
from pathlib import Path

def load_prices(ticker):
    file_path = Path(__file__).resolve().parent.parent.parent / "data" / f"{ticker}.csv"
    df = pd.read_csv(file_path, index_col="Date", parse_dates=True) 
    df = df.sort_index()
    return df
        
if __name__ == "__main__":
    prices = load_prices("MSFT")
    print(prices.head())
    print(len(prices))
