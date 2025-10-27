import sys
import pandas as pd
import matplotlib.pyplot as plt

import utils.stock_price_fetcher as spf
import utils.return_calculation as rc
import utils.correlation_analysis as cor
import modeling.monte_carlo_simulation as mc
import modeling.option_pricing as op
import utils.visualisation as vis


if __name__ == "__main__":

#First fetch data and calculate returns
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

#Then calculate covariance matrix and correlation matrix
    covariance_matrix, correlation_matrix = cor.calculate_correlation(stock_return_data)
    print('correlation matrix calculated')
    print(correlation_matrix)
    if not isinstance(stock_return_data.columns, pd.MultiIndex):
        print('Only one stock data fetched')

#Next, use covariance matrix to do monte carlo simulation
    return_data = stock_return_data['return']
    initial_prices = stock_data['Close'].iloc[-1]
    mean_returns_value = return_data.mean()
    simulations = 1000
    days = 252

    simulation_df = mc.run_monte_simulation(initial_prices, mean_returns_value, covariance_matrix, num_simulations=simulations, num_days=days)
    print('Monte Carlo simulation finished')
    print(simulation_df.head().iloc[:,:6])

#Calculate the option price
    all_sigmas = op.calculate_historical_volatility(stock_return_data)
    all_latest_prices = stock_data['Close'].iloc[-1] #要注意什么时候要series，什么时候要单个value，注意使用.item()
    expiration_date = '2025-12-26'
    risk_free_rate = 0.04
    dividend_yield = 0.0

    for ticker in tickers:
        print(f"\n========== Pricing Option for {ticker} ==========")

    # extract current stock data from pd.Series
        S = all_latest_prices[ticker]
        sigma = all_sigmas[ticker]
        K = S * 1.05

        print(f"Underlying Price (S): {S}")
        print(f"Strike Price (K): {K}")
        print(f"Expiration Date: {expiration_date}")
        print(f"Risk-free Rate (r): {risk_free_rate}")
        print(f"Annualized Volatility (sigma): {sigma}")

        option_values = op.eu_option_pricing(
            underlying_price=S,
            strike_price=K,
            expiration_data=expiration_date,
            risk_free_rate=risk_free_rate,
            volatility=sigma,
            dividend_yield=dividend_yield,
            option_type='c'
        )

        if option_values:
            print("\n--- Calculated Option Values ---")
            for key, value in option_values.items():
                print(f"{key.capitalize():<10}: {value:.4f}") # <10：alignment  .4f: keep 4 digits after decimal

# Visualization
# plot monte carlo simulation
    if simulation_df is not None:
        first_ticker = tickers[0]
        first_ticker_sim_df = simulation_df.loc[:, (slice(None), first_ticker)]
        vis.plot_monte_carlo(
            first_ticker_sim_df,
            title=f"Monte Carlo Simulation for {first_ticker}"
        )

        vis.simulation_price_distribution(
            simulation_df,
            title=f"Final Day Price Distribution ({simulations} simulations, {days} days)"
        )

        plt.show()