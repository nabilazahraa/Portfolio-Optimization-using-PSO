import numpy as np
import yfinance as yf
import pandas as pd
from pyswarm import pso
from datetime import datetime, timedelta

def calculate_portfolio_return(weights, returns):
    # Calculate the expected portfolio return
    portfolio_return = np.dot(weights, returns.mean()) * 252  # Assuming 252 trading days in a year
    
    return portfolio_return

def calculate_portfolio_volatility(weights, returns):
    # # Calculate the expected portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_volatility

def calculate_sharpe_ratio(weights, returns, risk_free_rate):
    rf_daily = (1+ risk_free_rate) ** (1/252) - 1
    portfolio_return = calculate_portfolio_return(weights, returns)
    portfolio_volatility = calculate_portfolio_volatility(weights, returns)
    sharpe_ratio = (portfolio_return - rf_daily) / portfolio_volatility
    return -sharpe_ratio  # Return negative for minimization in PSO

def calculate_downside_deviation(returns, target=0):
    underperformance = np.minimum(0, returns - target)
    return np.sqrt(np.mean(underperformance**2))

def calculate_sortino_ratio(weights, returns, risk_free_rate, target=0):
    rf_daily = (1+ risk_free_rate) **(1/252) - 1
    portfolio_return = calculate_portfolio_return(weights, returns)
    downside_deviation = calculate_downside_deviation(returns @ weights, target)
    sortino_ratio = (portfolio_return - rf_daily) / downside_deviation
    return -sortino_ratio  # Minimize negative Sortino for maximization in PSO


def pso_optimization(tickers, goal, start_date, end_date, n_particles=30, max_iter=200):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    daily_returns = data.pct_change().dropna()
    risk_free_rate = yf.download(['^IRX'], start=start_date, end=end_date)['Adj Close'].mean() / 100

    n_assets = len(tickers)
    bounds = [(0, 1) for _ in range(n_assets)]

    if goal == '1':
        objective = lambda w: calculate_sharpe_ratio(w, daily_returns, risk_free_rate)
        title = 'Maximizing Sharpe Ratio'
    elif goal == '2':
        objective = lambda w: calculate_portfolio_volatility(w, daily_returns)
        title = 'Minimizing Volatility'
    elif goal == '3':
        objective = lambda w: -calculate_portfolio_return(w, daily_returns)
        title = 'Maximizing Return'
    elif goal == '4':
        objective = lambda w: calculate_sortino_ratio(w, daily_returns, risk_free_rate)
        title = 'Maximizing Sortino Ratio'
    else:
        raise ValueError("Invalid optimization goal specified.")

    optimal_weights, optimal_value = pso(objective, [0] * n_assets, [1] * n_assets, 
                                         swarmsize=n_particles, omega=0.9, phip=2, phig=2, maxiter=max_iter, 
                                         minstep=1e-8, minfunc=1e-8,debug=True)

    optimal_weights /= np.sum(optimal_weights)

    associated_risk = calculate_portfolio_volatility(optimal_weights, daily_returns)
    associated_return = calculate_portfolio_return(optimal_weights, daily_returns)

    sorted_ticker_weights = sorted([(tickers[i], optimal_weights[i]) for i in range(len(tickers)) if optimal_weights[i] > 0.01], key=lambda x: x[1], reverse=True)

    print(f"\nOptimal Portfolio for {title}:\n")
    for ticker, weight in sorted_ticker_weights:
        print(f"| {ticker.rjust(7, ' ')} | {100 * weight:.1f}% |")

    results = {
        'optimization goal': goal,
        'sorted_ticker_weights': sorted_ticker_weights,
        'associated_risk': associated_risk,
        'associated_return': associated_return
    }

    print(f"\nAssociated Risk (Volatility): {associated_risk:.2%}")
    print(f"Associated Return: {associated_return:.2%}\n")

    if goal == '1':
        ratio_value = -optimal_value
        ratio_name = 'Sharpe Ratio'
    elif goal == '2':
        ratio_value = optimal_value
        ratio_name = 'Volatility'
    elif goal == '3':
        ratio_value = -optimal_value
        ratio_name = 'Return'
    elif goal == '4':
        ratio_value = -optimal_value
        ratio_name = 'Sortino Ratio'


    print(f"Associated {ratio_name}: {ratio_value:.2f}\n")
    return results


# Example usage:
tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "LLY", "AVGO", "JPM"]
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

goal = '2'  # Example: '1' for Sharpe Ratio, '2' for Volatility, etc.

results = pso_optimization(tickers, goal, start_date, end_date)
