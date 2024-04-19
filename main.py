import pandas as pd
import numpy as np
from Particle import Particle
from StockReturns import getStockReturns

# ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'JNJ', 'UNH', 'META', 'V', 'NVDA', 'XOM', 'PG', 'WMT', 'JPM', 'MA', 'LLY', 'HD', 'PFE', 'CVX', 'BAC', 'KO', 'ABBV', 'MRK', 'PEP', 'VZ', 'TMO', 'COST', 'AVGO', 'ABT', 'DHR', 'ORCL', 'MCD', 'ADBE', 'CSCO', 'CMCSA', 'CRM', 'DIS', 'TMUS', 'NKE', 'BMY', 'PM', 'UPS', 'INTC', 'NEE', 'T', 'WFC', 'TXN', 'RTX', 'QCOM']

tickers = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA']
start_date = '2020-01-01'
end_date = '2021-01-01'
daily_returns = getStockReturns(tickers, start_date, end_date)

# PSO parameters
n_iterations = 100
n_particles = 30
n_assets = len(tickers)
risk_free_rate = 0.02
w = 0.1  # inertia
c1 = 2 # cognitive parameter
c2 = 2  # social parameter

# Initialize the swarm
swarm = [Particle(n_assets) for _ in range(n_particles)]
global_best_value = float('inf')
global_best_position = None

# Run the PSO algorithm
for iteration in range(n_iterations):
    for particle in swarm:
        value = particle.evaluate(daily_returns, risk_free_rate)
        # Update the global best if needed
        if value < global_best_value:
            global_best_value = value
            global_best_position = np.copy(particle.position)

    for particle in swarm:
        particle.update_velocity_and_position(global_best_position, w, c1, c2)

    print(f"Iteration {iteration} - Best Sharpe Ratio: {-global_best_value}")

# The position of the global best particle gives us the weights of the optimal portfolio
optimal_weights = global_best_position
for stock in range(len(tickers)):
            if optimal_weights[stock] > 0.001:
                print('|' + str(tickers[stock]).rjust(7, ' '), 
                      '|' + '{:.1f}'.format(100 * round(optimal_weights[stock], 3) ).rjust(11, ' ') + '% |'
                      )
print("Optimal Weights:", optimal_weights)
