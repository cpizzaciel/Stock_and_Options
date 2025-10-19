import yfinance as yf

def fetch_stock_price_history(ticker, period = '1y', interval = '1d'):
    stock_data = yf.download(tickers = ticker, #Multiple stocks should use list or separate with space
             period= period,  # Conflict with start and end. Use only one way
             interval= interval,  # Minute data only 60 days. Hour data only 2 years
             actions = False, #Give dividends action or not
             threads = True, # Use multi-threads to increase download speed when multiple stocks
             ignore_tz = None, # ignore time zone or not
             group_by = 'ticker', # column or ticker, group by data type or stock
             auto_adjust = True, # auto adjust dividends and split, use True
             back_adjust = False, # No need to use this, auto adjust already
             repair = True, #repair false information from yahoo finance
             keepna = False, # keep missing data column or not
             progress = False, # progress bar
             prepost = False, # Include pre-market and post-market or not
             rounding = False,
             timeout = 10, # max waiting time
             multi_level_index = True) # keep it true for easier data processing later when multiple stocks
    return stock_data

if __name__ == '__main__':
    ticker_to_test = 'GOOG'
    data = fetch_stock_price_history(ticker_to_test, '1y', '1d')
    if data is not None and not data.empty:
        print(f"--- Data for {ticker_to_test} ---")
        print(data.head())
    else:
        print(f"Failed to fetch data for {ticker_to_test}.")
    print(data.head())