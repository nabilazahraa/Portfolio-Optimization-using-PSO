import numpy as np
import yfinance as yf
from StockReturns import * 
from Particle import *

class MultiObjectiveParticle:
    def __init__(self, n_assets):
        self.position = np.random.dirichlet(np.ones(n_assets), size=1)[0]
        self.velocity = np.zeros(n_assets)
        self.best_position = np.copy(self.position)
        self.best_returns = -float('inf')
        self.best_volatility = float('inf')

    def evaluate(self, returns, risk_free_rate):
        current_return = -calculate_sharpe_ratio(self.position, returns, risk_free_rate)
        current_volatility = calculate_portfolio_volatility(self.position, returns)
        # Check for personal best update
        if (self.is_better(current_return, self.best_returns, current_volatility, self.best_volatility)):
            self.best_position = np.copy(self.position)
            self.best_returns = current_return
            self.best_volatility = current_volatility
        return current_return, current_volatility

    def is_better(self, ret1, ret2, vol1, vol2):
        better_return = ret1 > ret2
        better_volatility = vol1 < vol2
        return better_return and better_volatility

    def update_velocity_and_position(self, global_best_position, w, c1, c2):
        inertia = w * self.velocity
        cognitive = c1 * np.random.random() * (self.best_position - self.position)
        social = c2 * np.random.random() * (global_best_position - self.position)
        self.velocity = inertia + cognitive + social
        self.position += self.velocity
        self.position = np.clip(self.position, 1e-3, 1-1e-3)  # Ensure valid weights
        self.position /= np.sum(self.position)

