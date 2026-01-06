from crewai.tools import BaseTool

class RiskCalculatorTool(BaseTool):
    name: str = "Risk Calculator"
    description: str = "Calculate position sizing and risk exposure."

    def _run(self, portfolio_str: str) -> str:
        # portfolio_str could be "Buying $AAPL at 150, stop 140, total capital 100000"
        # For this MVP, we will accept a query like "ticker=AAPL, price=150, stop_loss=140, portfolio_value=100000"
        # Or more simply, checks if a trade is safe.
        
        # Simplified logic for MVP
        try:
            # Mock risk logic
            # "Is it safe to buy 10% AAPL?" -> "Yes/No"
            return """
            Risk Analysis:
            1. Position Sizing: Recommended max 5% of portfolio per trade.
            2. Stop Loss: Recommend 5-8% below entry.
            3. Exposure: Check correlation with existing Tech holdings.
            
            Veridct: SAFE to proceed if position size < 5%.
            """
        except Exception as e:
            return f"Error calculating risk: {str(e)}"
