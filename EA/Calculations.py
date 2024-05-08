import numpy as np

def calculate_portfolio_return(weights, returns):
    # Calculate the expected portfolio return
    portfolio_return = np.dot(weights, returns.mean()) * 252  # Assuming 252 trading days in a year
    return portfolio_return

def calculate_portfolio_volatility(weights, returns):
    # Calculate the expected portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_volatility

def calculate_sharpe_ratio(weights, returns, risk_free_rate):
    portfolio_return = calculate_portfolio_return(weights, returns)
    portfolio_volatility = calculate_portfolio_volatility(weights, returns)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return -sharpe_ratio  # Return negative for minimization in PSO

def calculate_downside_deviation(returns, target=0):
    underperformance = np.minimum(0, returns - target)
    return np.sqrt(np.mean(underperformance**2))

def calculate_sortino_ratio(weights, returns, risk_free_rate, target=0):
    portfolio_return = calculate_portfolio_return(weights, returns)
    downside_deviation = calculate_downside_deviation(returns @ weights, target)
    sortino_ratio = (portfolio_return - risk_free_rate) / downside_deviation
    return -sortino_ratio  # Minimize negative Sortino for maximization in PSO

