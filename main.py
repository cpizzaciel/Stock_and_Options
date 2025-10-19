import utils.stock_price_fetcher as spf



if __name__ == "__main__":
    tickers = ['NVDA', 'KO']
    stock_data = spf.fetch_stock_price_history(tickers, '1y', '1d')
    if stock_data is not None and not stock_data.empty:
        print("--- Data in need ---")
        print(stock_data.head())
    else:
        print("--- Failed to fetch data ---")