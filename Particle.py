import numpy as np

def calculate_portfolio_return(weights, returns):
    # Calculate the expected portfolio return
    portfolio_return = np.sum(returns.mean() * weights) * 252  # Assuming 252 trading days in a year
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

def calculate_maximum_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1
    return -drawdown.min()  # Return positive value



# Implement the PSO algorithm
class Particle:
    def __init__(self, n_assets):
        self.position = np.random.dirichlet(np.ones(n_assets), size=1)[0]
        self.velocity = np.zeros(n_assets)
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')

    def evaluate(self, returns, risk_free_rate, optimize_for='1'):
        if optimize_for == '1':  # Sharpe Ratio
            value = calculate_sharpe_ratio(self.position, returns, risk_free_rate)
        elif optimize_for == '2':  # Volatility
            value = calculate_portfolio_volatility(self.position, returns)
        elif optimize_for == '3':  # Return (Maximizing)
            value = calculate_portfolio_return(self.position, returns)
            value = -value  # Maximizing, minimize negative
        elif optimize_for == '4':  # Sortino Ratio
            value = calculate_sortino_ratio(self.position, returns, risk_free_rate)
        elif optimize_for == '5':  # Maximum Drawdown
            value = calculate_maximum_drawdown(returns @ self.position)
        else:
            raise ValueError("Invalid optimization goal specified.")

        if value < self.best_value:
            self.best_value = value
            self.best_position = np.copy(self.position)

        return value


    def update_velocity_and_position(self, global_best_position, w, c1, c2):
        inertia = w * self.velocity
        cognitive = c1 * np.random.random() * (self.best_position - self.position)
        social = c2 * np.random.random() * (global_best_position - self.position)
        self.velocity = inertia + cognitive + social
        self.position += self.velocity
        # Ensure the position is a valid probability distribution again
        self.position = np.clip(self.position, 1e-3, 1-1e-3)  # Avoid 0 weights
        self.position /= np.sum(self.position)  # Normalize

