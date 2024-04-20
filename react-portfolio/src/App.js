import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
    const [tickers, setTickers] = useState('AAPL, MSFT, GOOG');
    const [startDate, setStartDate] = useState('2020-01-01');
    const [endDate, setEndDate] = useState('2021-01-01');
    const [riskFreeRate, setRiskFreeRate] = useState(0.02);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [goal] = useState('1')

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:5000/optimize', {
                tickers: tickers.split(', ').map(ticker => ticker.trim()),
                startDate,
                endDate,
                riskFreeRate,
                goal
            });
            setResult(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
        setLoading(false);
    };

    return (
        <div className="container mt-5">
            <h1>Portfolio Optimization Tool</h1>
            <form onSubmit={handleSubmit} className="mb-3">
                <div className="mb-3">
                    <label className="form-label">Tickers:</label>
                    <input type="text" className="form-control" value={tickers} onChange={(e) => setTickers(e.target.value)} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Start Date:</label>
                    <input type="date" className="form-control" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                </div>
                <div className="mb-3">
                    <label className="form-label">End Date:</label>
                    <input type="date" className="form-control" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Risk-Free Rate (%):</label>
                    <input type="number" className="form-control" value={riskFreeRate} step="0.01" onChange={(e) => setRiskFreeRate(parseFloat(e.target.value))} />
                </div>
                <button type="submit" className="btn btn-primary">Optimize Portfolio</button>
            </form>
            {loading && <p>Loading...</p>}
            {result && (
                <div>
                    <h3>Results</h3>
                    <p>Optimization Goal: {result.optimization_goal}</p>
                    {result.sorted_ticker_weights && (
                        <div>
                            <h4>Allocations:</h4>
                            {result.sorted_ticker_weights.map((item, index) => (
                                <p key={index}>{item[0]}: {item[1].toFixed(2)}%</p>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default App;
