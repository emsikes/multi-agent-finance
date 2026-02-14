"""
Quantitative Financial Analysis Tool

This module defines CrewAI-compatible tools for performing fundamental
and comparative stock analysis using Yahoo Finance data.

It provides:

- Structured input schemas via Pydantic for ticker validation.
- A fundamental analysis tool that retrieves key financial metrics
    (e.g., market cap, P/E ratios, EPS, beta, 52-week range).
- A performance comparison tool that calculates 12-month percentage
    returns between two equities.

The tools are designed for use in multi-agent financial research systems,
where structured market data must be retrieved, normalized, and passed
to downstream LLM agents for reasoning and investment analysis.
"""

from typing import Type, Dict, Any, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import yfinance as yf


class StockAnalysisInput(BaseModel):
    """
    Input schema for the fundamental analysis tool.

    Enforces that a give ticker symbol is input as a string.
    ... -> Elipses, dictates that this input is a required field
    """
    ticker: str = Field(...,
                        description="The stock ticker symbol (e.g. 'AAPL', 'MSFT')")


class CompareStocksInput(BaseModel):
    """
    Input schema for the compare stocks tool.

    Requires two distinct tickers to compare them with each other
    """
    ticker_a: str = Field(...,
                          description="The first stock ticker symbol to analyze")
    ticker_b: str = Field(...,
                          description="The second stock ticker symbol to compare")


class FundamentalAnalystTool(BaseModel):
    """
    CrewAI Tool that will extract the fundamental metrics for a stock.

    This tool will screen stocks providing the raw data, and will performance
    analysis to determine if the stock is over or under valued, volatile, etc.
    """
    name: str = "Fetch fundamental metrics"
    description: str = ("Returns key metrics for a specific tock ticker for quantatative analysis in a JSON \
                        formatted document.  This data will include P/E ration, beta volatility, market cap \
                        earnings per share, price to earnings ratio, and 52 week high and low")

    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, ticker: str) -> str:
        """
        Executes the data fetching from yahoo finance.

        Args: 
            ticker: (str)

        Returns:
            A stringified JSON dictionary that contains the selected matrics 
            or an error message if it failes
        """
        try:
            # Initialize the tocker object .info will hold stock info in a dictionary
            stock = yf.Ticker(ticker)
            info: Dict[str, Any] = stock.info

            # Select only the metrics we want for sending to the LLM
            metrics = {
                "Ticker": ticker.upper(),
                "Current Price": info.get("currentPrice", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "P/E Ratio (trailing)": info.get("trailingPE", "N/A"),
                "Forward P/E": info.get("forwardPE", "N/A"),
                "PEG Ration": info.get("pegRation", "N/A"),
                "Beta (Volatility)": info.get("beta", "N/A"),
                "EPS (trailing)": info.get("trailingEps", "N/A"),
                "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Analyst Recommendation": info.get("recommendationKey", "none")
            }

            return str(metrics)

        except Exception as e:
            return f"Error fetching fundamental data from Yahoo Finance for '{ticker}': str{e}"


class CompareStocksTool(BaseModel):
    """
    CrewAI tool that will calculate the relative performance between two assets.

    E.g. - which stock performed better over a 12 month period expressed in percent change in price.
    """
    name: str = "Compare Stock Performance"
    decription: str = ("Compares the historical performance of two stocks over the previous 365 days. \
                       Returns the percentage gain or loss for both assets.")

    args_schema: Type[BaseModel] = CompareStocksInput

    def _run(self, ticker_a: str, ticker_b: str) -> str:
        """
        Fetches the historical data and calculates the percentage return.

        Formula: (last price - first price) / (first price) * `100
        """
        try:
            tickers = f"{ticker_a} {ticker_b}"
            data = yf.download(tickers, period="1y", progress=False)['Close']

            # Helper function to calculate the overall return
            def calculate_return(symbol: str) -> float:
                # First day of 365 days we will review
                start_price = data[symbol].iloc[0]
                # Last day of 365 days we will review
                end_price = data[symbol].iloc[-1]
                return ((end_price - start_price) / start_price) * 100

            perf_a = calculate_return(ticker_a)
            perf_b = calculate_return(ticker_b)

            return (f"Performance Comparison (Previous 12 months)")

        except Exception as e:
            return f"Error comparing stocks: '{ticker_a}' and '{ticker_b}': str{e}"
