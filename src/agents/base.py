from abc import ABC, abstractmethod
from crewai import Agent

class BaseGryphonAgent(ABC):
    """
    Abstract Base Class for Gryphon Agents.
    All agents must implement the `create` method to return a crewai.Agent.
    """
    
    def __init__(self, llm=None):
        self.llm = llm

    @abstractmethod
    def create(self) -> Agent:
        """Creates and returns the configured CrewAI Agent."""
        pass
