from abc import ABC, abstractmethod

class BaseSearch(ABC):
    """Abstract interface for search providers."""
    
    @abstractmethod
    def search(self, query: str) -> str:
        """Execute a search query and return the results."""
        pass
