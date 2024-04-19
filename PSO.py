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

class Particle:
    def __init__(self, n_assets):
        self.position = np.random.dirichlet(np.ones(n_assets), size=1)[0]
        self.velocity = np.zeros(n_assets)
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')

    def evaluate(self, returns, risk_free_rate):
        value = calculate_sharpe_ratio(self.position, returns, risk_free_rate)
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
