from datetime import date
import pandas as pd
import numpy as np
from py_vollib.black_scholes_merton import black_scholes_merton as bsm
from py_vollib.black_scholes_merton.greeks.analytical import delta, gamma, vega, theta

# import tools:
from utils.stock_price_fetcher import fetch_stock_price_history
from utils.return_calculation import calculate_returns


def calculate_historical_volatility(stock_data: pd.DataFrame, window:int = 252):
    # calculate annualized volatility
    returns = calculate_returns(stock_data)['return']
    daily_std = returns.std()
    annualized_volatility = daily_std * np.sqrt(window)
    # See if it's a pandas.Series. Only need the value
    return annualized_volatility

def eu_option_pricing(
        underlying_price: float,
        strike_price: float,
        expiration_data: str, #format: "YYYY-MM-DD"
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float = 0.0,
# 'c' for call option, 'p' for put option
        option_type: str = 'c'

):
    today = date.today()
    expiry = date.fromisoformat(expiration_data)
    time_to_expiry = (expiry - today).days/ 365.25

    if time_to_expiry < 0:
        print('Error: Expiration date has passed')
        return None

    try:
        price = bsm(option_type, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
        d = delta(option_type, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
        g = gamma(option_type, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
        v = vega(option_type, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
        t = theta(option_type, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)

        return {
            'price': price,
            'delta': d,
            'gamma': g,
            'vega': v,
            'theta': t
        }
    except Exception as e:
        print(f"An error occurred during calculation: {e}")
        return None

if __name__ == '__main__':
    ticker = 'NVDA'
    hist_data = fetch_stock_price_history(ticker)

    #latest close price
    S = hist_data['Close'].iloc[-1].values[0]

    # historical volatility
    sigma = calculate_historical_volatility(hist_data)
    sigma = sigma.item()

    # set K, t, r manually
    K = S*1.05
    expiration = '2025-12-26'
    r = 0.04

    print(f"--- Pricing a Call Option for {ticker} ---")
    print(f"Underlying Price (S): {S}")
    print(f"Strike Price (K): {K}")
    print(f"Expiration Date: {expiration}")
    print(f"Risk-free Rate (r): {r}")
    print(f"Annualized Volatility (sigma): {sigma}")

    option_values = eu_option_pricing(S, K, expiration, r, sigma, 0,'c')

    if option_values:
        print("\n Calculated Option Pricing")
        for key, value in option_values.items():
            print(f"{key.capitalize()}: {value}")
