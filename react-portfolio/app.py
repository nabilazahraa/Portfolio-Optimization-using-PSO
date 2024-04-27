from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from optimize_portfolio import optimize_portfolio


app = Flask(__name__)
CORS(app)

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json()
        selected_tickers = data['tickers']
        start_date = data['startDate']
        end_date = data['endDate']
        optimization_goal = data['goal']
        # Convert start_date and end_date to datetime objects
        # start_date = start_date.strftime('%Y-%m-%d')
        # end_date = end_date.strftime('%Y-%m-%d')
        # start_date = datetime.strptime(start_date, '%Y-%m-%d')
        # end_date = datetime.strptime(end_date, '%Y-%m-%d')


        # Validate inputs
        if not selected_tickers or not optimization_goal:
            return jsonify({"error": "Missing tickers or optimization goal"}), 400

        # Call your portfolio optimization function
        results = optimize_portfolio(selected_tickers, start_date, end_date, optimization_goal)

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
