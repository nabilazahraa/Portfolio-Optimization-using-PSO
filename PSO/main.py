import pandas as pd
import numpy as np
from Particle import Particle
from StockReturns import getStockReturns
from Particle import calculate_portfolio_return, calculate_portfolio_volatility
from datetime import datetime, timedelta
from multiobjective import MultiObjectiveParticle
import matplotlib.pyplot as plt
import yfinance as yf
from optimize_portfolio import optimize_portfolio
import time

tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "LLY", "AVGO", "JPM"]
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
# dates = 2014-05-10 2024-05-07
print(start_date, end_date)
# start_date = '2015-01-01'
# end_date = '2024-01-01'
# def optimize_portfolio(tickers, goal, start_date, end_date,w=0.1, c1 =2, c2= 2, n_iterations=250, n_particles=100):
w = 0.9
c1 = 2
c2 = 2
n = 30
i =  250

# w= 0.7 
# c1= 2.5
# c2 = 1.5
# n= 30 
# i = 100

# w=0.5 
# c1=2
# c2 = 2
# n = 50
# i=250

#calculate time taken to run

results = optimize_portfolio(tickers,2, start_date, end_date,w =w, c1 =c1, c2=c2,  n_iterations=i, n_particles=n)

