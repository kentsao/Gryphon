import os
from dotenv import load_dotenv
from crewai import Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
# If using Groq/others via LiteLLM, we can just pass string model names to Agent, 
# but putting an LLM object gives more control.

from .agents.factory import ScoutAgent, AnalystAgent, RiskAgent, StrategistAgent
from .tasks import GryphonTasks

load_dotenv()

class GryphonEngine:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.llm = self._setup_llm()

    def _setup_llm(self):
        # Google Gemini Setup
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-1.5-flash") 
        
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in .env")
        
        return ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=api_key)

    def run(self):
        print(f"Starting Gryphon Engine for {self.ticker}...")
        
        # 1. Create Agents
        scout = ScoutAgent(self.llm).create()
        analyst = AnalystAgent(self.llm).create()
        risk = RiskAgent(self.llm).create()
        strategist = StrategistAgent(self.llm).create()
        
        # 2. Define Tasks
        tasks = GryphonTasks()
        
        t_scout = tasks.scout_task(scout, self.ticker)
        t_analyst = tasks.analyst_task(analyst, self.ticker)
        t_risk = tasks.risk_task(risk, self.ticker, context_tasks=[t_scout, t_analyst])
        t_strategist = tasks.strategist_task(strategist, self.ticker, context_tasks=[t_scout, t_analyst, t_risk])
        
        # 3. Assemble Crew
        crew = Crew(
            agents=[scout, analyst, risk, strategist],
            tasks=[t_scout, t_analyst, t_risk, t_strategist],
            process=Process.sequential,
            verbose=True
        )
        
        # 4. Kickoff
        result = crew.kickoff()
        return result
