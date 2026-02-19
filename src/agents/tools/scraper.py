"""
Web Intelligence and Sentiment Analysis Tool

This module provides a CrewAI-compatible tool for performing semantic
web searches and scraping market-relevant content using the Firecrawl API.

It enables:

- Structured query validation via Pydantic models.
- Retrieval of recent stock news, analyst commentary, and market sentiment.
- Extraction of full-page content in Markdown format for downstream analysis.

Designed for integration into multi-agent financial systems where
qualitative market signals complement quantitative data to support
investment research and decision-making workflows.
"""


from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from firecrawl import FireCrawlApp

from src.shared.config import settings


class FireCrawlSearchInput(BaseModel):
    """
    Defines the FireCrawl search query string
    """
    query: str = Field(...,
                       description="The search query string (e.g. 'latest NVDA analyst rating')")


class SentimentSearchTool(BaseTool):
    """
    Performs the semantic web search and returns the scraped content.
    This tool will use Firecrawl to return the top results and extract the full page
    content in Markdown format.
    """
    name: str = "Search Stock News"
    description: str = ("Searches the web for the latest news on stocks, \
                        recent analyst ratings, and general market sentiment \
                        for a given stock.  Returns a summary of the top 3 \
                        relevant articles.")

    args_schema: Type[BaseModel] = FireCrawlSearchInput

    def _run(self, query: str) -> str:
        """
        Executes a search using the Firecrawl API.

        Args: 
            query: (str): the search topic

        Returns:
            markdown formatted document of the top search results
        """
        if not settings.firecrawl_api_key:
            return "Error: Firecrawl API key not loaded from src.shared.config"

        try:
            app = FireCrawlApp(api_key=settings.firecrawl_api_key)
            # Perfoem web search: limit results to 3, return in markdown
            results = app.search(
                query=query,
                limit=3,
                scrape_options={"formats": ["markdown"]}
            )

            return str(results)

        except Exception as e:
            return f"Error executing the Firecrawl search: str{e}"
