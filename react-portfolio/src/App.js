import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; 
import Modal from 'react-modal';
import Chart from 'chart.js/auto'; // Import Chart.js library

Modal.setAppElement('#root');

function App() {
    const [tickers, setTickers] = useState(['MSFT', 'AAPL', 'NVDA', 'AMZN', 'META', 'GOOGL', 'LLY', 'AVGO', 'JPM', 'NFLX'])
    const [selectedTickers, setSelectedTickers] = useState([]);
    const [inputTicker, setInputTicker] = useState('');
    const [startDate, setStartDate] = useState('2015-01-01');
    const [endDate, setEndDate] = useState('2024-01-01');
    const [riskFreeRate, setRiskFreeRate] = useState(0.02);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [goal, setGoal] = useState('1')
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [showSummary, setShowSummary] = useState(false); // State to manage summary visibility
    const [pieChart, setPieChart] = useState(null); // State to hold the pie chart instance

    useEffect(() => {
        if (result && result.sorted_ticker_weights) {
            renderPieChart(result.sorted_ticker_weights);
        }
    }, [result]);

    

    const renderPieChart = (data) => {
        const ctx = document.getElementById('pieChart');
        if (ctx) {
            if (pieChart) {
                pieChart.destroy(); // Destroy existing chart instance
            }
            setPieChart(new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.map(item => item[0]),
                    datasets: [{
                        label: 'Allocations',
                        data: data.map(item => item[1] * 100), // Convert to percentage
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 152, 215, 0.7)',    
                            'rgba(255, 206, 86, 0.7)',   
                            'rgba(75, 180, 190, 0.9)',   
                            'rgba(153, 102, 255, 0.7)',  
                            'rgba(255, 159, 64, 0.7)',   
                            'rgba(155, 99, 132, 0.9)',   
                            'rgba(54, 162, 235, 0.7)',   
                            'rgba(255, 106, 56, 0.7)',    
                            'rgba(75, 192, 192, 0.7)'    
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            }));
        }
    };

    const handleTickerClick = (ticker) => {
        setInputTicker(ticker);
    };

    const handleInputChange = (event) => {
        setInputTicker(event.target.value);
    };

    const handleAddTicker = () => {
        setSelectedTickers([...selectedTickers, inputTicker]);
        setInputTicker('');
    };

    const handleClearTickers = () => {
        setSelectedTickers([]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:5000/optimize', {
                tickers: selectedTickers,
                startDate,
                endDate,
                riskFreeRate,
                goal
            });
            setResult(response.data);
            setModalIsOpen(true); // Open the modal after getting the result
            setShowSummary(true); // Show summary when result is available
        } catch (error) {
            console.error('Error fetching data:', error);
        }
        setLoading(false);
    };

    const handleRemoveTicker = (tickerToRemove) => {
        setSelectedTickers(selectedTickers.filter(ticker => ticker !== tickerToRemove));
    };

    const handleSelectAll = () => {
        setSelectedTickers(tickers);
    };

    return (
        <div className="app">
        <div className="container app-container">
            <h1 className="app-title">Portfolio Optimization Using PSO</h1>
            <form onSubmit={handleSubmit} className="mb-3">
            <div className="mb-3">
                <label className="form-label">Our Recommended Companies (click to select)</label>
                <div className='row-1'>
                <div className="d-flex flx-wrap">
                    {tickers.map((ticker, index) => (
                        <div key={index} className="m-2 ticker-item" onClick={() => handleTickerClick(ticker)}>
                            <img src={`/${ticker}.png`} alt={`${ticker} logo`} className="ticker-logo" />
                        </div>
                    ))}
                </div>
                </div>
                <label className="form-label-left">Input custom ticker</label>
                <input type="text" className="form-control" value={inputTicker} onChange={handleInputChange} />
                <div className='btn-row'>
                <button type="button" className="btn" onClick={handleAddTicker}>Add Ticker</button>
                <button type="button" className="btn" onClick={handleSelectAll}>Select All</button>
                </div>
            </div>

                <div className="mb-3">
                    {/* <label className="form-label">Selected Tickers:</label> */}
                    <div className="selected-tickers-list">
                        {selectedTickers.map((ticker, index) => (
                            <span key={index} className="badge bg-secondaryn m-1">
                                {ticker}
                                <button type="button" className="btn-close btn-close-white ms-2" onClick={() => handleRemoveTicker(ticker)}></button>
                            </span>
                        ))}
                    </div>
                    <div className='btn-row'>
                    <button type="button" className="btn" onClick={handleClearTickers}>Clear All</button>
                    </div>
                </div>
                <div className="mb-3 row">
                    <div className="col">
                        <label className="form-label-left">Start Date:</label>
                        <input type="date" className="form-control" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                    </div>
                    <div className="col">
                        <label className="form-label-left">End Date:</label>
                        <input type="date" className="form-control" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
                    </div>
                </div>
 
                <div className="row-1">
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">
                            Maximize Sharpe Ratio
                        </div>
                        <div className="card-body">
                            <p className="card-text">Optimizes the portfolio for maximum Sharpe Ratio, which represents the average return earned in excess of the risk-free rate per unit of volatility or total risk.</p>
                        </div>
                        <input type="radio" name="goal" value="1" checked={goal === '1'} onChange={(e) => setGoal(e.target.value)} className='radio-button'  />
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">
                            Minimize Volatility
                        </div>
                        <div className="card-body">
                            <p className="card-text">Optimizes the portfolio for minimum volatility, aiming to achieve the most stable returns by minimizing the standard deviation of the portfolio returns.</p>
                        </div>
                        <input type="radio" name="goal" value="2" checked={goal === '2'} onChange={(e) => setGoal(e.target.value)} className='radio-button' />
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">
                            Maximize Returns
                        </div>
                        <div className="card-body">
                            <p className="card-text">Optimizes the portfolio for maximum returns, aiming to achieve the highest possible return regardless of the risk.</p>
                        </div>
                        <input type="radio" name="goal" value="3" checked={goal === '3'} onChange={(e) => setGoal(e.target.value)} className='radio-button'  />
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">
                            Maximize Sortino Ratio
                        </div>
                        <div className="card-body">
                            <p className="card-text">Optimizes the portfolio for maximum return for a given level of downside risk. It is particularly useful as it only considers the downside risk, thus providing a more accurate measure of risk-adjusted returns.</p>
                        </div>
                        <input type="radio" name="goal" value="4" checked={goal === '4'} onChange={(e) => setGoal(e.target.value)} className='radio-button'  />
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">
                            MOPSO (Max Returns - Min Risk)
                        </div>
                        <div className="card-body">
                            <p className="card-text">Optimizes the portfolio for maximizing returns while minimizing risk. It uses a swarm-based algorithm (Multi Objective Particle Swarm Optimization) to find the optimal trade-off between these two conflicting objectives.</p>
                        </div>
                        <input type="radio" name="goal" value="5" checked={goal === '5'} onChange={(e) => setGoal(e.target.value)} className='radio-button' />
                    </div>
                </div>
            </div>
            <div className='btn-row'>
                <button type="submit" className="btn">Optimize Portfolio</button>
            </div>
            </form>
            {loading && <div className="loading-overlay"><div className="spinner"></div></div>}
            {/* <div className="pie-chart-container">
                    <canvas id="pieChart"></canvas>
            </div> */}
                <Modal
                    isOpen={modalIsOpen}
                    onRequestClose={() => setModalIsOpen(false)}
                    contentLabel="Results"
                    className="Modal"
                    overlayClassName="Overlay"
                >
                    <h2>Allocations</h2>
                    {result && result.sorted_ticker_weights && (
                        <div>
                            {result.sorted_ticker_weights.map((item, index) => (
                                <p key={index}>{item[0]}: {(item[1]*100).toFixed(2)}%</p>
                            ))}
                        </div>
                    )}
                    <button className="btn" onClick={() => setModalIsOpen(false)}>Close</button>
                </Modal>
                {showSummary && ( // Show summary when showSummary is true
                <div className="pie-chart-summary-container row-1">
                <div className="pie-chart-container">
                    <canvas id="pieChart"></canvas>
                </div>
                <div className="statistical-summary">
                    <h2>Statistical Summary</h2>
                    {result && (
                        <div>
                            <p>Associated Risk: {(result.associated_risk * 100).toFixed(2)}%</p>
                            <p>Associated Return: {(result.associated_return * 100).toFixed(2)}%</p>
                        </div>
                    )}
                </div>
            </div>
            )}
        </div>
        </div>
    );
}

export default App;
