# Calculate stock return rate for {ticker}

import pandas as pd
import numpy as np

from utils.stock_price_fetcher import fetch_stock_price_history

def calculate_returns(stock_data: pd.DataFrame, column_name: str = "Close"):
    if stock_data is None or stock_data.empty:
        print("Empty stock price data")
        return stock_data

    if isinstance(stock_data.columns, pd.MultiIndex):
        close_prices = stock_data[column_name]
        returns = close_prices.pct_change()
        for ticker in returns.columns:
            stock_data[('return',ticker)] = returns[ticker]

    else:
        if column_name in stock_data.columns:
            stock_data['return'] = stock_data[column_name].pct_change()
        else:
            print(f"{column_name} not found in stock price data")

    return stock_data

if __name__ == '__main__':
    print("--- Running test for return_calculation.py ---")
    stock_data = fetch_stock_price_history(['NVDA', 'KO'], '1y', '1d')
    stock_return_data = calculate_returns(stock_data)
    print(stock_return_data)