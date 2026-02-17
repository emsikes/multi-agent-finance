"""
Task Definitions for the crew:

Acts as a prompt engineering layer for agentic system.

Key features:
    Context injection - strategist explicitly waits for and recieves output from
    the Quant Agent to ensure data driven reasoning
"""

from crewai import Task, Agent


def create_tasks(quant_agent: Agent, strategist_agent: Agent, ticker: str) -> list[Task]:
    """
    Args:
        quant_agent: financial metrics
        strat_agent: news and synthesis
        ticer: stock symbol

    Returns:
        a list of talk object in the order of execution
    """
    quant_task = Task(
        description=(
            f"You are conducting a quantitative financial analysis for the stock ticker '{ticker}'.\n\n"

            "OBJECTIVE:\n"
            "Evaluate financial strength, valuation, volatility, and relative performance.\n\n"

            "INSTRUCTIONS:\n"
            "1. Use FundamentalAnalysisTool to retrieve:\n"
            "   - Price-to-Earnings (P/E) Ratio\n"
            "   - Earnings Per Share (EPS)\n"
            "   - Beta\n"
            "   - Market Capitalization\n\n"

            "2. Use CompareStocksTool to compare '{ticker}' vs 'SPY' over the last 12 months.\n"
            "   - Determine relative return performance\n"
            "   - Identify outperformance or underperformance\n\n"

            "3. Evaluate quantitative risk signals:\n"
            "   - Negative or declining EPS\n"
            "   - P/E significantly above sector average (> 2x market norm)\n"
            "   - Beta > 1.3 (high volatility)\n"
            "   - Extreme drawdowns vs SPY\n\n"

            "4. Synthesize findings into a structured summary.\n\n"

            "OUTPUT FORMAT:\n"
            "Return the following sections clearly labeled:\n"
            "- Valuation Metrics\n"
            "- Volatility Profile\n"
            "- Relative Performance vs SPY\n"
            "- Quantitative Risk Flags\n"
            "- Overall Quantitative Assessment (2–4 sentences, objective and data-driven)\n\n"

            "Do not include speculation, news, or qualitative commentary."
        ),
        expected_output=(
            "Return a clearly structured quantitative analysis report containing:\n\n"
            "1. Valuation Metrics:\n"
            "   - P/E Ratio (numeric)\n"
            "   - EPS (numeric)\n"
            "   - Market Capitalization (numeric with units)\n\n"
            "2. Volatility Profile:\n"
            "   - Beta (numeric)\n"
            "   - Interpretation of volatility vs market\n\n"
            "3. 1-Year Performance Comparison:\n"
            "   - % return of the stock over last 12 months\n"
            "   - % return of SPY over last 12 months\n"
            "   - Clear statement of outperformance or underperformance\n\n"
            "4. Quantitative Risk Flags:\n"
            "   - Bullet list of any numerical red flags identified\n"
            "   - If none, explicitly state 'No major quantitative red flags detected.'\n\n"
            "5. Overall Quantitative Assessment:\n"
            "   - 2–4 concise, objective sentences summarizing financial strength\n\n"
            "Strictly data-driven. No qualitative news, opinions, or speculation."
        ),
        agent=quant_agent
    )

    recommendation_task = Task(
        description=(
            f"You are the Chief Investment Strategist evaluating stock ticker '{ticker}'.\n\n"

            "OBJECTIVE:\n"
            "Produce a disciplined, evidence-based investment recommendation by synthesizing\n"
            "quantitative fundamentals with qualitative sentiment and news catalysts.\n\n"

            "INPUTS:\n"
            "- Quantitative report from the Quantitative Analyst\n"
            "- Real-time qualitative signals from SentimentSearchTool\n\n"

            "INSTRUCTIONS:\n"
            "1. Carefully review the quantitative analysis:\n"
            "   - Valuation metrics\n"
            "   - Volatility profile\n"
            "   - Relative performance vs SPY\n"
            "   - Identified quantitative risk flags\n\n"

            "2. Use SentimentSearchTool to retrieve the 3 most recent relevant developments\n"
            "   for '{ticker}' including:\n"
            "   - Earnings announcements\n"
            "   - Leadership changes\n"
            "   - Regulatory or legal issues\n"
            "   - Product launches or partnerships\n"
            "   - Analyst upgrades/downgrades\n\n"

            "3. Evaluate qualitative tone:\n"
            "   - Positive catalyst\n"
            "   - Neutral / informational\n"
            "   - Negative risk event\n\n"

            "4. Synthesize using disciplined conflict resolution:\n"
            "   - Strong fundamentals + positive/neutral news → Bullish bias\n"
            "   - Strong fundamentals + negative catalyst → Cautious or Hold\n"
            "   - Weak fundamentals + positive hype → Skeptical stance\n"
            "   - Weak fundamentals + negative news → Bearish bias\n\n"

            "5. Weight fundamentals higher than short-term news unless\n"
            "   the news represents material structural risk (e.g., major lawsuit,\n"
            "   fraud investigation, regulatory ban).\n\n"

            "OUTPUT FORMAT (STRICT):\n"
            "- Quantitative Summary (2–3 sentences)\n"
            "- Qualitative Catalyst Summary (2–3 sentences)\n"
            "- Risk Assessment (bullet points)\n"
            "- Final Verdict: BUY / HOLD / SELL\n"
            "- Confidence Level: Low / Medium / High\n"
            "- 3–5 sentence rationale grounded in evidence\n\n"

            "Do not speculate. Do not exaggerate sentiment. Do not rely on hype.\n"
            "Base the decision strictly on retrieved data."
        ),
        expected_output=(
            "Return a structured Markdown investment recommendation report with the following EXACT sections:\n\n"

            "## Quantitative Summary\n"
            "- 2–3 concise sentences summarizing valuation, volatility, and relative performance.\n\n"

            "## Qualitative Catalyst Summary\n"
            "- Summary of the 3 most relevant recent developments.\n"
            "- Clearly indicate whether tone is Positive, Neutral, or Negative.\n\n"

            "## Risk Assessment\n"
            "- Bullet list of key risks (financial, volatility, regulatory, structural).\n"
            "- If no material risks are identified, explicitly state: 'No material structural risks identified.'\n\n"

            "## Final Verdict\n"
            "One of: BUY / HOLD / SELL\n\n"

            "## Confidence Level\n"
            "One of: Low / Medium / High\n\n"

            "## Investment Rationale\n"
            "3–5 sentences explaining the decision.\n"
            "- Must reconcile quantitative data with qualitative catalysts.\n"
            "- Must justify why BUY, HOLD, or SELL was selected.\n\n"

            "Constraints:\n"
            "- Do not speculate beyond retrieved data.\n"
            "- Do not exaggerate sentiment.\n"
            "- Keep total response under 400 words.\n"
            "- Maintain objective, professional tone."
        ),
        agent=strategist_agent,
        context=[quant_task],
        output_file=f"investment_report_{ticker}.md"
    )

    return [quant_task, recommendation_task]
