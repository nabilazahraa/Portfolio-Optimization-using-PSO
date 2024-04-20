import numpy as np


def calculate_sharpe_ratio(weights, returns, risk_free_rate):
    # Calculate the expected portfolio return
    portfolio_return = np.sum(returns.mean() * weights) * 252  # Assuming 252 trading days in a year
    # Calculate the expected portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    # Calculate the Sharpe Ratio
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    # We will maximize Sharpe Ratio by minimizing negative Sharpe Ratio
    return -sharpe_ratio

def calculate_portfolio_volatility(weights, returns):
    # Calculate the expected portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_volatility


# Implement the PSO algorithm
class Particle:
    def __init__(self, n_assets):
        self.position = np.random.dirichlet(np.ones(n_assets), size=1)[0]
        self.velocity = np.zeros(n_assets)
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')

    def evaluate(self, returns, risk_free_rate, optimize_for='sharpe_ratio'):
        if optimize_for == '1':
            value = calculate_sharpe_ratio(self.position, returns, risk_free_rate)
        elif optimize_for == '2':
            value = calculate_portfolio_volatility(self.position, returns)
            # Since we want to minimize volatility, we return it directly without negation
        else:
            raise ValueError("Invalid optimization goal specified.")
        # Update the personal best if needed
        if optimize_for == 'sharpe ratio' and value < self.best_value:
            self.best_value = value
            self.best_position = np.copy(self.position)
        elif optimize_for == 'volatility' and value < self.best_value:
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

