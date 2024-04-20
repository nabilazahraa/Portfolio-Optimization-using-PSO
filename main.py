import pandas as pd
import numpy as np
from Particle import Particle
from StockReturns import getStockReturns
from Particle import calculate_portfolio_return, calculate_portfolio_volatility

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

while True:
    optimize_goal = input("Enter optimization goal:\n (1) Sharpe Ratio\n (2) Volatility (Minimizing Risk)\n (3) Return (Maximizing Return)\n (4) Sortino Ratio\n (5) Maximum Drawdown\nEnter your choice (type 'exit' to quit): ").lower()
    if optimize_goal == 'exit':
        break

    # Initialize the swarm
    swarm = [Particle(n_assets) for _ in range(n_particles)]
    global_best_value = float('inf')
    global_best_position = None

    # Run the PSO algorithm
    for iteration in range(n_iterations):
        for particle in swarm:
            value = particle.evaluate(daily_returns, risk_free_rate, optimize_goal)
            # Update the global best if needed
            if value < global_best_value:
                global_best_value = value
                global_best_position = np.copy(particle.position)

        for particle in swarm:
            particle.update_velocity_and_position(global_best_position, w, c1, c2)

        if(optimize_goal == '1'):
            print(f"Iteration {iteration} - Best Sharpe Ratio: {-global_best_value}")
        elif(optimize_goal == '2'):
            print(f"Iteration {iteration} - Best Volatility: {global_best_value}")
        elif(optimize_goal == '3'):
            print(f"Iteration {iteration} - Best Return: {-global_best_value}")
        elif(optimize_goal == '4'):
            print(f"Iteration {iteration} - Best Sortino Ratio: {-global_best_value}")
        elif(optimize_goal == '5'):
            print(f"Iteration {iteration} - Best Maximum Drawdown: {global_best_value}")

    optimal_weights = global_best_position
    if optimize_goal == '3':  # If the goal was to maximize return
        associated_risk = calculate_portfolio_volatility(global_best_position, daily_returns)
        print(f"Associated risk (volatility) for maximized returns: {associated_risk * 100:.2f}%")
    elif optimize_goal == '2':  # If the goal was to minimize risk
        associated_return = calculate_portfolio_return(global_best_position, daily_returns)
        print(f"Associated return for minimized risk: {associated_return * 100:.2f}%")
    for stock in range(len(tickers)):
        if optimal_weights[stock] > 0.001:
            print('|' + str(tickers[stock]).rjust(7, ' '), '|' + '{:.1f}'.format(100 * round(optimal_weights[stock], 3) ).rjust(11, ' ') + '% |')
    print("Optimal Weights:", optimal_weights)
