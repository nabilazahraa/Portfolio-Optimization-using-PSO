import pandas   as pd
import numpy    as np
import datetime as dt
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas   as pd
import yfinance as yf 



def pullStockData(StockTickers, minDate, maxDate, interval='1mo'):
    stockMetrics = ["Adj Close"]    
    PulledStocks = pd.DataFrame(columns = stockMetrics)
    count = 0
    outOf = len(StockTickers)
    # Pull each stocks
    for stock in StockTickers:  
        count += 1 # Keep track
        # Get the stock ticker over the date range
        print('\nDownloading', stock, '- Progress:', count, '/', outOf)
        stockTicker = yf.download(stock, start=minDate, end=maxDate, 
                                  interval=interval)
        stockTicker = stockTicker.reset_index()
        
        stockTicker["Stock"] = stock
        PulledStocks = pd.concat([PulledStocks, stockTicker])  
    stockMetrics = ["Stock", "Date"] + stockMetrics
    PulledStocks = PulledStocks[stockMetrics] 
    
    PulledStocks = PulledStocks.rename(columns = {'Stock':     'stock',
                                                  'Date':      'period',
                                                  'Adj Close': 'adjClose'})
    
    return PulledStocks.dropna() 

maxDate = datetime.now().strftime('%Y-%m-%d')                   # Max date to pull from
minDate = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')# Min date to pull from

# List of stock tickers to pull data from (top 50 market cap stocks companies in US S&P 500)
StockTickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "LLY", "AVGO", "JPM"]
MONTHS_IN_YEAR = 1 # The number of months in a year, IF USING NON-ANNUALIZED DATA!

lowerBound        = 0   # no weight in a stock
upperBound        = 1   # Max weight in stock


# Pull in data based on input parameters (Stock tickers, date range)
RawStockData = pullStockData(StockTickers, minDate, maxDate)
print(RawStockData)

# # Pivot so that each stock is its own column
RawStockDataPivot = RawStockData.copy().pivot(index='period', columns='stock',  values='adjClose')
print(RawStockDataPivot)
# RawStockDataPivot.to_csv('RawStockDataPivot.csv')
# returns = RawStockDataPivot.copy()
# returns[StockTickers] = returns[StockTickers] /  returns[StockTickers].shift(12) - 1
# returns = returns.dropna()
returns = RawStockDataPivot.pct_change(12)

print(returns)


# # =============================================================================
# Import T-Bill (monthly)
# T-Bill Ref: https://finance.yahoo.com/quote/%5EIRX/history/
# # =============================================================================

# Get the average risk free rate
# T_Bill = pullStockData(['^IRX'], minDate, maxDate)

# Get the annualized average t-bill rate over date range
# Need over date range to get risk adjusted returns (Sharpe Ratio)
# riskFreeRate = T_Bill['adjClose'].mean() / 100 # 100%
# print(riskFreeRate)