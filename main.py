import sys

import utils.stock_price_fetcher as spf
import utils.return_calculation as rc


if __name__ == "__main__":
    tickers = ['NVDA', 'KO']
    stock_data = spf.fetch_stock_price_history(tickers, '1y', '1d')
    if stock_data is None or stock_data.empty:
        error_message = f"Fatal Error: Failed to fetch data for ticker '{tickers}'. Program cannot continue."
        sys.exit(error_message)
    else:
        print("stock data fetched successfully")
    stock_return_data = rc.calculate_returns(stock_data)
    print("stock data with returns:")
    print(stock_return_data)
