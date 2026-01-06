from crewai import Agent
from .base import BaseGryphonAgent
from ..tools.duck_search import DuckSearchTool
from ..tools.market import YFinanceNewsTool, YFinancePriceTool, YFinanceHistoryTool
from ..tools.analysis import TechnicalAnalysisTool
from ..tools.risk import RiskCalculatorTool

class ScoutAgent(BaseGryphonAgent):
    def create(self) -> Agent:
        return Agent(
            role='The Scout (Collector)',
            goal='Gather comprehensive market news, social sentiment, and earnings reports for the target stock.',
            backstory="""You are an expert market news analyst. Your job is to scour the web and financial news sources 
            to find the most relevant and up-to-date information about a stock. You look for sentiment (positive/negative), 
            upcoming earnings, and major announcements. You do not care about charts, only the narrative.""",
            tools=[DuckSearchTool(), YFinanceNewsTool()],
            verbose=True,
            llm=self.llm
        )

class AnalystAgent(BaseGryphonAgent):
    def create(self) -> Agent:
        return Agent(
            role='The Analyst (Researcher)',
            goal='Perform deep technical analysis on the stock price and trends.',
            backstory="""You are a veteran technical analyst. You look at charts, moving averages, RSI, and MACD. 
            You don't care about the news, only the numbers and price action. You provide data-driven insights 
            on whether the stock is overbought, oversold, or trending.""",
            tools=[YFinancePriceTool(), YFinanceHistoryTool(), TechnicalAnalysisTool()],
            verbose=True,
            llm=self.llm
        )

class RiskAgent(BaseGryphonAgent):
    def create(self) -> Agent:
        return Agent(
            role='The Guard (Risk Manager)',
            goal='Ensure capital preservation and evaluate portfolio exposure.',
            backstory="""You are the risk manager. Your only job is to protect the portfolio. You evaluate 
            proposed trades against risk limits. You are conservative and skeptical. You check if the position 
            size is too big or if the trade is too risky.""",
            tools=[RiskCalculatorTool()],
            verbose=True,
            llm=self.llm
        )

class StrategistAgent(BaseGryphonAgent):
    def create(self) -> Agent:
        return Agent(
            role='The Strategist (Manager)',
            goal='Synthesize reports from the team and make a final Buy/Sell/Hold recommendation.',
            backstory="""You are the Chief Investment Officer. You read the reports from the Scout, Analyst, and Guard. 
            You synthesize their conflicting information into a coherent decision. You must provide a clear 
            Verdict (BUY/SELL/HOLD), the Rationale, and any specific execution instructions. You write for the human user.""",
            tools=[], # Pure synthesis, relies on context from others
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
