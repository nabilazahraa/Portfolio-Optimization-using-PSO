import pandas as pd
import numpy as np
from Particle import Particle
from StockReturns import getStockReturns
from Particle import calculate_portfolio_return, calculate_portfolio_volatility
from datetime import datetime, timedelta
from multiobjective import MultiObjectiveParticle
import matplotlib.pyplot as plt
import yfinance as yf

tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "LLY", "AVGO", "JPM"]
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
print("Fetching data...")
daily_returns = getStockReturns(tickers, start_date, end_date)

# PSO parameters
n_iterations = 250
n_particles = 100
n_assets = len(tickers)
T_Bill = yf.download(['^IRX'], start_date, end_date)
risk_free_rate = T_Bill['Adj Close'].mean()/100


# risk_free_rate = T_Bill.iloc[-1].mean()/100
# risk_free_rate = 0.02
w = 0.1  # inertia
c1 = 2 # cognitive parameter
c2 = 2  # social parameter

# w = 0.5  # inertia
# c1 = 0.3 # cognitive parameter
# c2 = 0.4  # social parameter

while True:
    optimize_goal = input("Enter optimization goal:\n (1) Sharpe Ratio\n (2) Volatility (Minimizing Risk)\n (3) Return (Maximizing Return)\n (4) Sortino Ratio\n (5) Multiobjective\n Enter your choice (type 'exit' to quit): ").lower()
    # n_iterations = int(input("Enter number of iterations: "))
    if optimize_goal == 'exit':
        break
    if optimize_goal in '5':
        # Initialize the swarm
        swarm = [MultiObjectiveParticle(n_assets) for _ in range(n_particles)]
        # Perform iterations
        for iteration in range(n_iterations):
            global_best_returns = -float('inf')
            global_best_volatility = float('inf')
            global_best_position = None

            for particle in swarm:
                ret, vol = particle.evaluate(daily_returns)
                if particle.is_better(ret, global_best_returns, vol, global_best_volatility):
                    global_best_position = particle.position
                    global_best_returns = ret
                    global_best_volatility = vol
                # print(f"Iteration {iteration}: Return: {ret}, Volatility: {vol}")

            for particle in swarm:
                particle.update_velocity_and_position(global_best_position, w, c1, c2)
            
            print(f"Iteration {iteration}: Return: {global_best_returns}, Volatility: {global_best_volatility}")


        # Determine the optimal weights from best positions
        optimal_weights = global_best_position

    elif optimize_goal in ['1', '2', '3', '4']:
        # Initialize the swarm
        swarm = [Particle(n_assets) for _ in range(n_particles)]
        global_best_value = float('inf')
        global_best_position = None
        best_values= [] 

        # Run the PSO algorithm
        for iteration in range(n_iterations):
            for particle in swarm:
                value = particle.evaluate(daily_returns, risk_free_rate, optimize_goal)
                # Update the global best if needed
                if value < global_best_value:
                    global_best_value = value
                    global_best_position = np.copy(particle.position)
            best_values.append(-global_best_value)
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
            

        optimal_weights = global_best_position
        if optimize_goal == '3':  # If the goal was to maximize return
            associated_risk = calculate_portfolio_volatility(global_best_position, daily_returns)
            print(f"\nAssociated risk (volatility) for maximized returns: {associated_risk * 100:.2f}% \n")
        elif optimize_goal == '2':  # If the goal was to minimize risk
            associated_return = calculate_portfolio_return(global_best_position, daily_returns)
            print(f"\nAssociated return for minimized risk: {associated_return * 100:.2f}% \n")
            
    # Create a list of (ticker, weight) tuples
    ticker_weights = [(tickers[i], optimal_weights[i]) for i in range(len(tickers)) if optimal_weights[i] > 0.01]

    # Sort the list in descending order by weight
    sorted_ticker_weights = sorted(ticker_weights, key=lambda x: x[1], reverse=True)

    # Print the sorted list
    for ticker, weight in sorted_ticker_weights:
        print(f"| {ticker.rjust(7, ' ')} | {100 * weight:.1f}% |")
    
    plt.figure(figsize=(10, 5))
    plt.plot(best_values, marker='o', linestyle='-', color='b')
    plt.title('Convergence of PSO Optimization (Best Sharpe Ratio)')
    plt.xlabel('Iteration')
    plt.ylabel('Best Sharpe Ratio')
    plt.grid(True)
    plt.show()
