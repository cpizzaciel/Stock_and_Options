# Stock and Options

A new project for stock price collection, return calculation,
Monte-Carlo simulation, and options pricing.

## 1. Data collection and primary processing

Added stock price data fetching function. 
The stock price data is in stock_data DataFrame in the main.py file.

Added stock daily return calculation.
the stock price data with calculated return data is in the stock_return_data DataFrame in the main.py file.


Added calculation of correlation matrix between different stocks.
Both the covariance matrix and the correlation matrix are returned with the correlation_analysis function.


## 2. Modeling and Simulation

Added monte-carlo simulation function

Added option pricing function
updated this function for multiple tickers handling.
the "calculate_historical_volatility" function return a pd.Series of stock volatility.
If calculate options of different underlying, keep it as a pd.Series.
If calculate only one option, add .item() to get the scaler number.

the"eu_option_pricing" function calculates option price and the Greeks.
expiration date is in format: "YYYY-MM-DD".
option_type: str = 'c', 'c' for call option, 'p' for put option
default dividends is 0.
        