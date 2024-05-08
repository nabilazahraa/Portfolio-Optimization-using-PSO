import numpy as np
import random
from Calculations import *
import yfinance as yf
from EA import initialize_population, evaluate_population, selection, crossover, mutation   
from datetime import datetime, timedelta

import time

def getStockReturns(tickers, startDate, end_date):
    data = yf.download(tickers, start=startDate, end=end_date)
    # We'll consider adjusted closing prices
    adjustedClose = data['Adj Close']
    returns = adjustedClose.pct_change().dropna()
    return returns

def optimize_portfolio_ga(selected_tickers, start_date, end_date, optimization_goal, num_generations=100, population_size=50):
    daily_returns = getStockReturns(selected_tickers, start_date, end_date)
    n_assets = len(selected_tickers)
    T_Bill = yf.download(['^IRX'], start_date, end_date)
    risk_free_rate = T_Bill['Adj Close'].mean() / 100
    start = time.time()
    # GA parameters
    num_parents = population_size // 2
    offspring_size = population_size - num_parents
    mutation_rate = 0.1
    
    # Initialize population
    population = initialize_population(n_assets, population_size)
    best_values_over_generations = []
    
    for generation in range(num_generations):
        evaluations = evaluate_population(population, daily_returns, risk_free_rate, optimization_goal)
        parents = selection(population, evaluations, num_parents)
        offspring = crossover(parents, offspring_size)
        population = parents + mutation(offspring, mutation_rate)
        best_value = min(evaluations)
        best_values_over_generations.append(best_value)
        
        if optimization_goal == '1':
            print(f"Generation {generation} - Best Sharpe Ratio: {-best_value}")
        elif optimization_goal == '2':
            print(f"Generation {generation} - Best Volatility: {best_value}")
        elif optimization_goal == '3':
            print(f"Generation {generation} - Best Return: {-best_value}")
        elif optimization_goal == '4':
            print(f"Generation {generation} - Best Sortino Ratio: {-best_value}")

    # Find the best solution
    best_index = np.argmin(evaluations)
    best_weights = population[best_index]
    associated_risk = calculate_portfolio_volatility(best_weights, daily_returns)*100
    associated_return = calculate_portfolio_return(best_weights, daily_returns)*100
    end = time.time()
    # Create a list of (ticker, weight) tuples
    ticker_weights = [(selected_tickers[i], best_weights[i]*100) for i in range(len(selected_tickers)) if best_weights[i] > 0.01]
    # Sort the list in descending order by weight
    sorted_ticker_weights = sorted(ticker_weights, key=lambda x: x[1], reverse=True)
    total = end - start
    results = {
        'optimization goal': optimization_goal,
        'sorted_ticker_weights': sorted_ticker_weights,
        'associated_risk': associated_risk,
        'associated_return': associated_return
    }
    print("Time taken: ", total)
    return results, best_values_over_generations

tickers = ['MSFT', 'AAPL', 'NVDA', 'AMZN', 'META', 'GOOGL', 'LLY', 'AVGO', 'JPM', 'NFLX']
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
results, best_values = optimize_portfolio_ga(tickers, start_date, end_date, '1', num_generations=1000, population_size=50)
print(results)