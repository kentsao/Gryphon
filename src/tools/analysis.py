import yfinance as yf
import pandas_ta as ta
from crewai.tools import BaseTool

class TechnicalAnalysisTool(BaseTool):
    name: str = "Technical Analyst"
    description: str = "Perform technical analysis (RSI, SMA, MACD) on a stock ticker."

    def _run(self, ticker: str) -> str:
        try:
            # Fetch data (requires more than just last 20 days for some indicators)
            stock = yf.Ticker(ticker)
            df = stock.history(period="6mo")
            
            if df.empty:
                return f"No data found for {ticker}."

            # Calculate Indicators
            # RSI
            df.ta.rsi(length=14, append=True)
            # SMA 50 and 200
            df.ta.sma(length=50, append=True)
            df.ta.sma(length=200, append=True)
            # MACD
            df.ta.macd(append=True)

            # Get latest values
            latest = df.iloc[-1]
            
            report = f"""
            Technical Analysis Report for {ticker}:
            - Price: {latest['Close']:.2f}
            - RSI (14): {latest['RSI_14']:.2f}
            - SMA (50): {latest['SMA_50']:.2f}
            - SMA (200): {latest['SMA_200']:.2f}
            - MACD Line: {latest['MACD_12_26_9']:.2f}
            - MACD Signal: {latest['MACDs_12_26_9']:.2f}
            - MACD Histogram: {latest['MACDh_12_26_9']:.2f}
            """
            
            # Simple interpretation help for the LLM
            rsi = latest['RSI_14']
            if rsi > 70:
                report += "\nInterp: Overbought (RSI > 70)"
            elif rsi < 30:
                report += "\nInterp: Oversold (RSI < 30)"
            
            return report

        except Exception as e:
            return f"Error performing analysis on {ticker}: {str(e)}"
