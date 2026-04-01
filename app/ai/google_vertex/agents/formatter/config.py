"""Configuration settings for the Formatter Agent."""
from dataclasses import dataclass
from google.genai import types


@dataclass
class FormatterConfig:
    """
    Configuration settings for the Formatter Agent.
    """

    temperature: float = 0.0
    max_output_tokens: int = 8000
    top_p: float = 0.0
    instruction: str = (
        "You are a Data Structuring Agent for the Finly investment platform.\n\n"
        "### TASK\n"
        "The session state contains a key 'formatted_data' with raw financial analysis "
        "from the Research Agent. Structure it into the PortfolioBreakdown JSON schema exactly.\n\n"
        "### RULES\n"
        "1. Read the analysis from session state key 'formatted_data'.\n"
        "2. Extract all stocks, sectors, recommendations, and performance metrics.\n"
        "3. Map every field to the PortfolioBreakdown schema exactly — do not skip or rename fields.\n"
        "4. If a value is missing or unavailable, use null — do not guess or fabricate.\n"
        "5. OUTPUT: A single valid JSON object only. No markdown, no code blocks, no explanation.\n")

    def get_content_config(self) -> types.GenerateContentConfig:
        """Returns the content generation configuration for the agent."""
        return types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
            response_mime_type="application/json",
        )
