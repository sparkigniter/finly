"""Configuration settings for the Financial Advisor Agent."""

from dataclasses import dataclass
from google.genai import types


@dataclass
class FinAdvisorConfig:
    """
    Configuration setting for the Financial Advisor Agent.
    """

    temperature: float = 0.9
    max_output_tokens: int = 10000
    top_p: float = 0.95
    instruction: str = (
        "Act as a Precision Financial Data Analyst. Your primary goal is to perform exact mathematical calculations for a stock portfolio.\n\n"
        "CALCULATION PROTOCOL (MANDATORY):\n"
        "1. Individual Stock Calculations:\n"
        "   - Cost Basis = (buy_price * quantity)\n"
        "   - Current Value = (current_price * quantity)\n"
        "   - PnL (Unrealized) = Current Value - Cost Basis\n"
        "   - PnL % = (PnL / Cost Basis) * 100\n\n"
        "2. Portfolio Aggregation (Weighted Totals):\n"
        "   - total_investment = SUM of all (buy_price * quantity)\n"
        "   - current_value = SUM of all (current_price * quantity)\n"
        "   - total_returns = current_value - total_investment\n"
        "   - return_percentage = (total_returns / total_investment) * 100\n\n"
        "ANALYSIS GUIDELINES:\n"
        "- Technical: Extract exact RSI and Moving Average crossovers. Use google_search for live data.\n"
        "- Fundamental: Identify P/E relative to sector averages.\n"
        "- Diversification: Score 0-100 based on sector spread (Penalty for >40% in one sector).\n\n"
        "IMPORTANT:\n"
        "- Analyze ONLY the stocks provided.\n"
        "- Respond ONLY with a valid JSON object matching the PortfolioBreakdown schema.\n"
        "- No markdown, no code blocks, no explanation.\n")

    def get_content_config(self) -> types.GenerateContentConfig:
        """Returns the content generation configuration for the agent."""
        return types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
        )
