import yfinance as yf

def getStockReturns(tickers, startDate, end_date):
    data = yf.download(tickers, start=startDate, end=end_date)
    # We'll consider adjusted closing prices
    adjustedClose = data['Adj Close']
    returns = adjustedClose.pct_change().dropna()
    return returns

# tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN']  # Example tickers
# start_date = '2020-01-01'
# end_date = '2021-01-01'
# daily_returns = getStockReturns(tickers, start_date, end_date)
# print(daily_returns)