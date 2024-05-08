import yfinance as yf
from datetime import datetime, timedelta

def getStockReturns(tickers, startDate, end_date):
    data = yf.download(tickers, start=startDate, end=end_date)
    # We'll consider adjusted closing prices
    adjustedClose = data['Adj Close']
    returns = adjustedClose.pct_change().dropna()
    return returns


tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "LLY", "AVGO", "JPM"]
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
daily_returns = getStockReturns(tickers, start_date, end_date)
print(daily_returns)