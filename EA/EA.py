import numpy as np
import random
from Calculations import *
def initialize_population(n_assets, population_size):
    population = []
    for _ in range(population_size):
        weights = np.random.rand(n_assets)
        weights /= weights.sum()  # Normalize to ensure the sum of weights is 1
        population.append(weights)
    return population

def evaluate_population(population, returns, risk_free_rate, goal):
    evaluations = []
    for weights in population:
        if goal == '1':  # Sharpe Ratio
            value = calculate_sharpe_ratio(weights, returns, risk_free_rate)
        elif goal == '2':  # Volatility
            value = calculate_portfolio_volatility(weights, returns)
        elif goal == '3':  # Return (Maximizing)
            value = -calculate_portfolio_return(weights, returns)  # Negate to maximize
        elif goal == '4':  # Sortino Ratio
            value = calculate_sortino_ratio(weights, returns, risk_free_rate)
        else:
            raise ValueError("Invalid optimization goal specified.")
        evaluations.append(value)
    return evaluations

def selection(population, evaluations, num_parents):
    selected_parents = [population[i] for i in np.argsort(evaluations)[:num_parents]]
    return selected_parents

def crossover(parents, offspring_size):
    offspring = []
    num_parents = len(parents)
    for k in range(offspring_size):
        parent1_idx = k % num_parents
        parent2_idx = (k + 1) % num_parents
        crossover_point = np.random.randint(1, len(parents[0]) - 1)
        offspring.append(np.concatenate((parents[parent1_idx][:crossover_point], parents[parent2_idx][crossover_point:])))
    return offspring

def mutation(offspring, mutation_rate=0.1):
    for i in range(len(offspring)):
        if np.random.rand() < mutation_rate:
            mutation_point = np.random.randint(len(offspring[i]))
            offspring[i][mutation_point] = np.random.rand()
        offspring[i] /= offspring[i].sum()  # Re-normalize
    return offspring

