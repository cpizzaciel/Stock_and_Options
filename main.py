import sys
import pandas as pd

import utils.stock_price_fetcher as spf
import utils.return_calculation as rc
import utils.correlation_analysis as cor
import modeling.monte_carlo_simulation as mc


if __name__ == "__main__":
    tickers = ['NVDA', 'KO', 'GOOG']
    stock_data = spf.fetch_stock_price_history(tickers, '1y', '1d')
    if stock_data is None or stock_data.empty:
        error_message = f"Fatal Error: Failed to fetch data for ticker '{tickers}'. Program cannot continue."
        sys.exit(error_message)
    else:
        print("stock data fetched successfully")
    stock_return_data = rc.calculate_returns(stock_data)
    print("stock data with returns:")
    print(stock_return_data.head())


    covariance_matrix, correlation_matrix = cor.calculate_correlation(stock_return_data)
    print('correlation matrix calculated')
    print(correlation_matrix)
    if not isinstance(stock_return_data.columns, pd.MultiIndex):
        print('Only one stock data fetched')

    return_data = stock_return_data['return']
    initial_prices = stock_data['Close'].iloc[-1]
    mean_returns_value = return_data.mean()
    simulations = 1000
    days = 252

    simulation_df = mc.run_monte_simulation(initial_prices, mean_returns_value, covariance_matrix)
    print('Monte Carlo simulation finished')
    print(simulation_df.head().iloc[:,:6])
