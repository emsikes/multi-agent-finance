"""
CrewAI Agents definition module.

Defines the AI personas that will execute the financial analysis workflow.
Each Agent is equipped with a distinct set of tools and backstory.

Agents:
    Quantatative Analysis Agent: focuses on financial metrics

Investment Strategist:
    Qualatative Analysis Agent: focuses on qualatative news, sentiment, recent news 
"""

from typing import Tuple
from crewai import Agent

from src.agents.tools.finance import FundamentalAnalystTool, CompareStocksTool
from src.agents.tools.scraper import SentimentSearchTool


def create_agents() -> Tuple[Agent, Agent]:
    """
    Create CrewAI Agents

    Returns:
        A tuple containing: quant_agent, strategist_agent
    """
    # Quantatative Analyst Agent
    quant_agent = Agent(
        role="Senior Quantitative Analyst",
        goal="Evaluate valuation, financial strength, and historical performance using objective financial data.",
        backstory=(
            "You are a disciplined quantitative analyst. You rely strictly on financial metrics and historical price data. "
            "You evaluate valuation (P/E, forward P/E, PEG), profitability (EPS), scale (market cap), volatility (beta), "
            "and 12-month price performance. You ignore news, narratives, and speculation. "
            "Your analysis is concise, data-driven, and ends with a clear valuation stance: "
            "Undervalued, Fairly Valued, or Overvalued — supported only by numbers."
        ),
        verbose=True,
        memory=True,
        tools=[
            FundamentalAnalystTool(),
            CompareStocksTool()
        ],
        allow_delegation=False
    )

    # Strategist Agent: uses Firecrawl and explains 'why' the numbers are what they are
    strategist_agent = Agent(
        role="Chief Investment Strategist",
        goal="Integrate quantitative findings with market sentiment and current developments to form an actionable recommendation.",
        backstory=(
            "You are a macro-aware investment strategist. You interpret earnings trends, analyst ratings, leadership changes, "
            "sector momentum, and market sentiment. You explain why the numbers look the way they do. "
            "You combine the Quantitative Analyst findings with recent news and sentiment signals. "
            "Your output concludes with a decisive BUY, HOLD, or SELL recommendation and a brief risk assessment."
        ),
        verbose=True,
        memory=True,
        tools=[
            SentimentSearchTool()
        ],
        allow_delegation=False
    )

    return quant_agent, strategist_agent
