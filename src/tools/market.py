import yfinance as yf
from crewai.tools import BaseTool

class YFinanceNewsTool(BaseTool):
    name: str = "Market News Finder"
    description: str = "Get the latest news for a specific stock ticker using Yahoo Finance."

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            if not news:
                return f"No news found for {ticker}."
            
            formatted_news = []
            for item in news[:5]: # Top 5 news
                title = item.get('title', 'No Title')
                link = item.get('link', '#')
                publisher = item.get('publisher', 'Unknown')
                formatted_news.append(f"- {title} ({publisher}): {link}")
            
            return "\n".join(formatted_news)
        except Exception as e:
            return f"Error fetching news for {ticker}: {str(e)}"

class YFinancePriceTool(BaseTool):
    name: str = "Stock Price Checker"
    description: str = "Get the current price and basic info for a stock ticker."

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            currency = info.get('currency', 'USD')
            return f"Current price of {ticker}: {price} {currency}"
        except Exception as e:
            return f"Error fetching price for {ticker}: {str(e)}"

class YFinanceHistoryTool(BaseTool):
    name: str = "Stock Price History"
    description: str = "Get historical price data for a stock ticker for the last 1 month."

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            # Default to 1 month for MVP analysis
            history = stock.history(period="1mo")
            if history.empty:
                return f"No history found for {ticker}."
            
            # Return last 5 days as a sample string, or summary?
            # Creating a CSV-like string for the Analyst to read
            return history.tail(20).to_string() # Last 20 trading days
            
        except Exception as e:
            return f"Error fetching history for {ticker}: {str(e)}"
