from google.adk import Agent
from google.adk.tools import google_search_tool
from google.genai import types
from dataclasses import dataclass, field
from typing import Optional
from app.ai.google_vertex.agents.formatter.schemas.response import PortfolioBreakdown


@dataclass
class FinAdvisorConfig:
    """
        Configuration setting for the Financial Advisor Agent.
    """
    temperature: float = 0.0
    max_output_tokens: int = 8000
    top_p: float = 0.95
    instruction: str = (
        "As a financial advisor, analyze the provided stocks.\n"
        "1. Calculate gains/losses.\n"
        "2. Search for latest news/dividends for each ticker using google_search.\n"
        "3. Give recommendations (Hold/Sell/Buy More) with reasons.\n"
        "4. Give technical and fundamental indicator trends for each stock.\n\n"
        "IMPORTANT:\n"
        "- Analyze ONLY the stocks provided. DO NOT add extra stocks.\n"
        "- Respond ONLY with a valid JSON object matching the PortfolioBreakdown schema.\n"
        "- No markdown, no code blocks, no explanation.\n"
    )

    def get_content_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p
        )