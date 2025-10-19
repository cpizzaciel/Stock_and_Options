# Calculate covariance matrix and correlation coefficient
import pandas as pd

from utils.stock_price_fetcher import fetch_stock_price_history
from utils.return_calculation import calculate_returns

def calculate_correlation(stock_return_data_df):
    return_df = stock_return_data_df['return']
    corr_df = return_df.corr()
    cov_df = return_df.cov()
    return cov_df, corr_df

if __name__ == '__main__':
    test_tickers = ['NVDA', 'KO','GOOG']
    print(f"--- Running standalone test for correlation_analysis.py with tickers: {test_tickers} ---")
    stock_data = fetch_stock_price_history(test_tickers,'1y','1d')
    if stock_data is not None and not stock_data.empty:
        stock_return_data = calculate_returns(stock_data)
        if isinstance(stock_return_data.columns, pd.MultiIndex):
            correlation_matrix = calculate_correlation(stock_return_data)
            print('correlation matrix calculated')
            print(correlation_matrix)
        else:
            print('Only one stock data fetched')
    else:
        print('No data fetched')
