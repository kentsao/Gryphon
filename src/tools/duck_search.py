from crewai.tools import BaseTool
from duckduckgo_search import DDGS

class DuckSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Useful for searching the internet to find current news, sentiment, and market information."

    def _run(self, query: str) -> str:
        """Execute the search."""
        try:
            results = DDGS().text(query, max_results=5)
            if not results:
                return "No results found."
            
            formatted_results = []
            for result in results:
                formatted_results.append(f"Title: {result['title']}\nLink: {result['href']}\nSnippet: {result['body']}\n")
            
            return "\n---\n".join(formatted_results)
        except Exception as e:
            return f"Error performing search: {str(e)}"
