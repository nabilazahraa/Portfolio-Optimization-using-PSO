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

    def evaluate(self, returns):
        current_return = -calculate_sharpe_ratio(self.position, returns, 0.02)
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


tickers = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'JNJ']
start_date = '2020-01-01'
end_date = '2021-01-01'
daily_returns = getStockReturns(tickers, start_date, end_date)

# Example of running the PSO
n_assets = len(tickers)
particles = [MultiObjectiveParticle(n_assets) for _ in range(30)]
for particle in particles:
    ret, vol = particle.evaluate(daily_returns)
    print(f"Return: {ret}, Volatility: {vol}")

for stock in range(len(tickers)):
        if particle.best_position[stock] > 0.01:
            print('|' + str(tickers[stock]).rjust(7, ' '), '|' + '{:.1f}'.format(100 * round(particle.best_position[stock], 3) ).rjust(11, ' ') + '% |')
