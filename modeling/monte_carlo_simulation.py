import numpy as np
import pandas as pd

from utils.stock_price_fetcher import fetch_stock_price_history
from utils.return_calculation import calculate_returns

def run_monte_simulation(initial_price: pd.Series,
                         mean_returns: pd.Series,
                         cov_matrix: pd.DataFrame,
                         num_simulations: int = 1000,
                         num_days: int = 252 ):

    num_stocks = len(initial_price)
    tickers = initial_price.index

    s0 = initial_price.to_numpy()
    mu = mean_returns.to_numpy()

    try:
        L = np.linalg.cholesky(cov_matrix)
    except np.linalg.LinAlgError:
        print("Error: Covariance matrix is not positive definite.")
        return None

    simulation_results = np.zeros((num_days + 1, num_simulations, num_stocks)) # define the shape of the simulation
    simulation_results[0,:,:] = s0 #broadcast the initial stock prices to all simulations
    for day in range(1, num_days + 1):
        Z = np.random.standard_normal((num_simulations, num_stocks))
        correlated_randoms = L@Z.T

        daily_returns = mu + correlated_randoms.T

        simulation_results[day,:,:] = simulation_results[day - 1,:,:] * (1 + daily_returns)

    multi_index_cols = pd.MultiIndex.from_product(
        [range(num_simulations), tickers],
        names=['simulation', 'tickers']
    )

    results_reshaped = simulation_results.reshape(num_days + 1, -1)
    final_df = pd.DataFrame(results_reshaped, columns=multi_index_cols)

    return final_df

if __name__ == '__main__':
    print("--- Running a standalone test for Monte Carlo Simulation ---")
    test_tickers = ['NVDA', 'KO', 'GOOG']
    hist_data = fetch_stock_price_history(test_tickers)
    return_data = calculate_returns(hist_data)['return']
    initial_prices = hist_data['Close'].iloc[-1]
    mean_returns_value = return_data.mean()
    covariance_matrix = return_data.cov()
    simulations = 1000
    days = 252

    simulation_df = run_monte_simulation(initial_prices, mean_returns_value, covariance_matrix)
    if simulation_df is not None:
        print(f"\n--- Simulation successful! Generated {simulations} paths for {days} days. ---")
        print("Resulting DataFrame shape:", simulation_df.shape)
        print("Data preview (showing first 5 days for first 2 simulations):")
        print(simulation_df.head().iloc[:, :6])
