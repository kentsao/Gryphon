import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_data(tickers: list[str], period="2y") -> pd.DataFrame:
    """Fetches historical adjusted close prices for tickers + SPY benchmark."""
    all_tickers = tickers + ["SPY"]
    # yfinance allows space-separated tickers
    # Use 'Close' as newer yfinance versions might default to auto_adjust=True or similar
    data = yf.download(all_tickers, period=period, progress=False)
    
    # Handle MultiIndex if present (Price, Ticker)
    if isinstance(data.columns, pd.MultiIndex):
        # specific handling for 'Close' or 'Adj Close'
        if 'Adj Close' in data.columns.get_level_values(0):
             return data['Adj Close']
        elif 'Close' in data.columns.get_level_values(0):
             return data['Close']
        else:
             # Fallback: just return the first level if it matches tickers? 
             # Or maybe it has no Price level if single ticker? (But we always have SPY)
             return data.xs('Close', axis=1, level=0, drop_level=True)
             
    # Fallback for single index (older versions or single ticker)
    if "Adj Close" in data:
        return data["Adj Close"]
    return data["Close"]

def calculate_portfolio_metrics(holdings: dict[str, float]) -> dict:
    """
    Calculates portfolio metrics based on share counts.
    
    Args:
        holdings: Dict mapping ticker symbol to number of shares. 
                  e.g., {"AAPL": 10, "TSLA": 5}
    
    Returns:
        Dict containing:
        - total_value
        - beta
        - volatility
        - sharpe_ratio
        - max_drawdown
        - asset_allocation (dict of weights)
    """
    if not holdings:
        return {"error": "No holdings provided"}

    tickers = list(holdings.keys())
    
    # 1. Fetch Data
    try:
        prices = fetch_data(tickers)
    except Exception as e:
        return {"error": f"Failed to fetch market data: {str(e)}"}

    if prices.empty:
        return {"error": "No price data found"}

    # 2. Calculate Current Value & Weights
    latest_prices = prices.iloc[-1]
    portfolio_value = 0.0
    weights = {}
    
    for t in tickers:
        # Handle case where ticker might be missing in data
        if t not in latest_prices:
            continue
        val = latest_prices[t] * holdings[t]
        portfolio_value += val
        
    if portfolio_value == 0:
        return {"error": "Portfolio value is zero"}

    for t in tickers:
        if t in latest_prices:
            weights[t] = (latest_prices[t] * holdings[t]) / portfolio_value

    # 3. Calculate Returns
    returns = prices.pct_change().dropna()
    
    # Portfolio Daily Returns = Sum(Weight_i * Return_i)
    # We construct portfolio return series
    portfolio_returns = pd.Series(0, index=returns.index)
    for t, w in weights.items():
        if t in returns.columns:
            portfolio_returns += returns[t] * w
            
    benchmark_returns = returns["SPY"]
    
    # 4. Calculate Metrics
    
    # Beta
    # Covariance(Port, SPY) / Variance(SPY)
    covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    beta = covariance / benchmark_variance
    
    # Volatility (Annualized)
    # Daily Std Dev * Sqrt(252)
    daily_vol = np.std(portfolio_returns)
    volatility = daily_vol * np.sqrt(252)
    
    # Sharpe Ratio (Assuming risk-free rate ~ 4%)
    # (Mean Return - Risk Free) / Volatility
    risk_free_daily = 0.04 / 252
    excess_daily_return = portfolio_returns.mean() - risk_free_daily
    sharpe_ratio = (excess_daily_return / daily_vol) * np.sqrt(252)
    
    # Max Drawdown
    cumulative_returns = (1 + portfolio_returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    return {
        "total_value": round(portfolio_value, 2),
        "beta": round(beta, 2),
        "volatility": round(volatility, 2),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown": round(max_drawdown, 2),
        "weights": {k: round(v, 2) for k, v in weights.items()}
    }

if __name__ == "__main__":
    # Quick Test
    test_port = {"AAPL": 10, "NVDA": 5, "MSFT": 5}
    print("Testing with:", test_port)
    metrics = calculate_portfolio_metrics(test_port)
    print("Metrics:", metrics)
