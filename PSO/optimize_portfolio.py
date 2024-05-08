import pandas as pd
import numpy as np
from Particle import Particle
from StockReturns import getStockReturns
from Particle import calculate_portfolio_return, calculate_portfolio_volatility
from datetime import datetime, timedelta
from multiobjective import MultiObjectiveParticle
import matplotlib.pyplot as plt
import yfinance as yf
import os
import time


def optimize_portfolio(tickers, goal, start_date, end_date,w=0.5, c1 =2, c2= 2, n_iterations=250, n_particles=50):
    print("Fetching data...")
    daily_returns = getStockReturns(tickers, start_date, end_date)

    # PSO parameters
    T_Bill = yf.download(['^IRX'], start_date, end_date)
    risk_free_rate = T_Bill['Adj Close'].mean() / 100

    # w = 0.1  # inertia
    # c1 = 2  # cognitive parameter
    # c2 = 2  # social parameter

    while True:
        optimize_goal = input("Enter optimization goal:\n (1) Sharpe Ratio\n (2) Volatility (Minimizing Risk)\n (3) Return (Maximizing Return)\n (4) Sortino Ratio\n (5) Multiobjective\n Enter your choice (type 'exit' to quit): ").lower()
        if optimize_goal == 'exit':
            break

        returns_list = []
        volatility_list = []

        if optimize_goal == '5':
            # Initialize the swarm
            swarm = [MultiObjectiveParticle(len(tickers)) for _ in range(n_particles)]
            # Perform iterations
            global_best_returns = -float('inf')
            global_best_volatility = float('inf')
            global_best_position = None
            
            for iteration in range(n_iterations):
                for particle in swarm:
                    ret, vol = particle.evaluate(daily_returns)
                    returns_list.append(ret)
                    volatility_list.append(vol)
                    if particle.is_better(ret, global_best_returns, vol, global_best_volatility):
                        global_best_position = particle.position
                        global_best_returns = ret
                        global_best_volatility = vol

                for particle in swarm:
                    particle.update_velocity_and_position(global_best_position, w, c1, c2, iteration, n_iterations, swarm)

                print(f"Iteration {iteration}: Return: {global_best_returns}, Volatility: {global_best_volatility}")

            optimal_weights = global_best_position
            associated_risk = calculate_portfolio_volatility(global_best_position, daily_returns)
            associated_return = calculate_portfolio_return(global_best_position, daily_returns)
            

        elif optimize_goal in ['1', '2', '3', '4']:
            # Initialize the swarm
            swarm = [Particle(len(tickers)) for _ in range(n_particles)]
            global_best_value = float('inf')
            global_best_position = None
            best_values = []
            start = time.time()
            # Run the PSO algorithm
            for iteration in range(n_iterations):
                for particle in swarm:
                    value = particle.evaluate(daily_returns, risk_free_rate, optimize_goal)
                    returns_list.append(calculate_portfolio_return(particle.position, daily_returns))
                    volatility_list.append(calculate_portfolio_volatility(particle.position, daily_returns))
                    # Update the global best if needed
                    if value < global_best_value:
                        global_best_value = value
                        global_best_position = np.copy(particle.position)
                best_values.append(-global_best_value)
                for particle in swarm:
                    # w = w_max - (w_max - w_min) * (iteration / max_iter)
                    # c1 = 1.5 + 1 * (iteration / max_iter)
                    # c2 = 2.5 - 1 * (iteration / max_iter)
                    particle.update_velocity_and_position(global_best_position, w, c1, c2, iteration, n_iterations, swarm)

                if optimize_goal == '1':
                    print(f"Iteration {iteration} - Best Sharpe Ratio: {-global_best_value}")
                elif optimize_goal == '2':
                    print(f"Iteration {iteration} - Best Volatility: {global_best_value}")
                elif optimize_goal == '3':
                    print(f"Iteration {iteration} - Best Return: {-global_best_value}")
                elif optimize_goal == '4':
                    print(f"Iteration {iteration} - Best Sortino Ratio: {-global_best_value}")

            optimal_weights = global_best_position
            end = time.time()
            total = end - start
        associated_risk = calculate_portfolio_volatility(global_best_position, daily_returns)
        associated_return = calculate_portfolio_return(global_best_position, daily_returns)
        # Create a list of (ticker, weight) tuples
        ticker_weights = [(tickers[i], optimal_weights[i]) for i in range(len(tickers)) if optimal_weights[i] > 0.01]

        # Sort the list in descending order by weight
        sorted_ticker_weights = sorted(ticker_weights, key=lambda x: x[1], reverse=True)

        # Print the sorted list
        for ticker, weight in sorted_ticker_weights:
            print(f"| {ticker.rjust(7, ' ')} | {100 * weight:.1f}% |")
        
        results = {
        'optimization goal': optimize_goal,
        'sorted_ticker_weights': sorted_ticker_weights,
        'associated_risk': associated_risk,
        'associated_return': associated_return
            }

        print("associated_risk: ", associated_risk)
        print("associated_return: ", associated_return)
        print("Time taken: ", total)
        # if optimize_goal =='5':
        #     # Plot volatility list vs iterations along with return
        #     plt.figure(figsize=(10, 5))
        #     plt.plot(volatility_list, marker='o', linestyle='-', color='b', label='Volatility')
        #     plt.xlabel('Iteration')
        #     plt.ylabel('Volatility (Risk)', color='b')  # Label for the left y-axis
        #     plt.tick_params(axis='y', labelcolor='b')   # Adjust color of left y-axis labels
        #     plt.grid(True)
        #     plt.ylim(min(returns_list) * 0.9, max(returns_list) * 1.1)


        #     # Create a twin Axes sharing the xaxis
        #     plt.twinx()

        #     # Plot return
        #     plt.plot(returns_list, marker='o', linestyle='-', color='r', label='Return')
        #     plt.ylabel('Return', color='r')  # Label for the right y-axis
        #     plt.tick_params(axis='y', labelcolor='r')   # Adjust color of right y-axis labels

        #     # Add legend
        #     plt.legend(loc='upper left')

        #     plt.title('Convergence of PSO Optimization: Risk vs Return')
        #     convergence_file = os.path.join('images', 'convergence_plot.png')
        #     plt.savefig(convergence_file)
        #     plt.show()

        # else:
        #     plt.figure(figsize=(10, 5))
        #     plt.plot(best_values, marker='o', linestyle='-', color='b')
        #     plt.title(f'Convergence of PSO Optimization (Best {"Sharpe Ratio" if optimize_goal == "1" else "Volatility" if optimize_goal == "2" else "Return" if optimize_goal == "3" else "Sortino Ratio"})')
        #     plt.xlabel('Iteration')
        #     plt.ylabel(f'Best {"Sharpe Ratio" if optimize_goal == "1" else "Volatility" if optimize_goal == "2" else "Return" if optimize_goal == "3" else "Sortino Ratio"}')
        #     plt.grid(True)
        #     convergence_file = os.path.join('images', 'convergence_plot.png')
        #     plt.savefig(convergence_file)
        #     plt.show()

        # plt.scatter(volatility_list, returns_list, c='b', marker='o')
        # plt.title('Risk vs Return Scatter Plot')
        # plt.xlabel('Volatility (Risk)')
        # plt.ylabel('Return')
        # plt.grid(True)

        # convergence_file = os.path.join('images', 'risk-return.png')
        # plt.savefig(convergence_file)
        # plt.show()

        # # Bar Plot 
        # optimal_weights = global_best_position
        # plt.figure(figsize=(10, 5))
        # plt.bar(tickers, optimal_weights)
        # plt.ylim(0, max(optimal_weights) * 1.1)
        # plt.xlabel('Tickers')
        # plt.ylabel('Weights')
        # plt.title('Optimal Portfolio Allocation')
        # convergence_file = os.path.join('images', 'allocations.png')
        # plt.savefig(convergence_file)
        # plt.show()

