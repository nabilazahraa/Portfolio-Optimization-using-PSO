from flask import Flask, render_template, request
from optimize_portfolio import optimize_portfolio

app = Flask(__name__)

tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "LLY", "AVGO", "JPM"]

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        selected_tickers = request.form.getlist('tickers')
        optimization_goal = request.form['optimization_goal']
        results = optimize_portfolio(selected_tickers, optimization_goal)
        return render_template('index.html', tickers=tickers, results=results)
    return render_template('index.html', tickers=tickers, results=results)

if __name__ == '__main__':
    app.run(debug=True)
