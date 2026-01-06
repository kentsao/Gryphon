from crewai import Task

class GryphonTasks:
    def scout_task(self, agent, ticker):
        return Task(
            description=f"""
            Collect the latest news, market sentiment, and major headlines for {ticker}.
            1. Search for recent news articles (last 7 days).
            2. Identify the general sentiment (Bullish/Bearish/Neutral).
            3. Look for any upcoming events (Earnings, Product Launches).
            4. Summarize the top 3 drivers moving the stock.
            """,
            expected_output="A concise bullet-point summary of news and sentiment.",
            agent=agent
        )

    def analyst_task(self, agent, ticker):
        return Task(
            description=f"""
            Perform a technical analysis on {ticker}.
            1. Get the current price and history.
            2. specific technical indicators (RSI, MACD, Moving Averages).
            3. Identify support and resistance levels if possible (or just trend).
            4. Determine the technical signal (Buy/Sell/Wait).
            """,
            expected_output="A technical report with key indicators and a trend signal.",
            agent=agent
        )

    def risk_task(self, agent, ticker, context_tasks):
        return Task(
            description=f"""
            Evaluate the risk of entering or holding a position in {ticker}.
            1. Review the analysis from the Scout and Analyst.
            2. Assess if the trade fits within general risk parameters (Max 5% allocation).
            3. Suggest a stop-loss level based on volatility (implied by the Analyst's report).
            """,
            expected_output="A risk assessment report with position sizing and stop-loss recommendations.",
            agent=agent,
            context=context_tasks # Tasks to wait/read from
        )

    def strategist_task(self, agent, ticker, context_tasks):
        return Task(
            description=f"""
            Make a final investment recommendation for {ticker}.
            1. Synthesize the News (Scout), Technicals (Analyst), and Risk (Guard).
            2. Resolve any conflicts (e.g., Good News but Bad Chart).
            3. Provide a clear VERDICT: BUY, SELL, or HOLD.
            4. Write a brief rationale explaining the decision.
            """,
            expected_output="A final Markdown report with Verdict, Rationale, and Action Plan.",
            agent=agent,
            context=context_tasks
        )
