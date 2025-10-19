import sys

import utils.stock_price_fetcher as spf
import utils.return_calculation as rc


if __name__ == "__main__":
    tickers = ['NVDA', 'KO']
    stock_data = spf.fetch_stock_price_history(tickers, '1y', '1d')
    if stock_data is None or stock_data.empty:
        print("--- Failed to fetch data ---")
        sys.exit()
    else:
        print("stock data fetched successfully")
    stock_return_data = rc.calculate_returns(stock_data)
    print("stock data with returns:")
    print(stock_return_data)
