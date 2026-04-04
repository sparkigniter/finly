"""Configuration settings for the Formatter Agent."""

from dataclasses import dataclass
from google.genai import types


@dataclass
class FormatterConfig:
    """
    Configuration settings for the Formatter Agent.
    """

    temperature: float = 0.2
    max_output_tokens: int = 8000
    top_p: float = 0.0
    instruction: str = (
        "You are a Data Structuring Agent for the Finly investment platform.\n\n"
        "### TASK\n"
        "The session state contains a key 'formatted_data' with raw financial analysis. "
        "Structure it into the PortfolioBreakdown JSON schema exactly.\n\n"
        "### RULES\n"
        "1. Map every field to the PortfolioBreakdown schema—do not skip technical or fundamental fields.\n"
        "2. If a numeric value (like rsi_value) is mentioned in text, cast it to a float.\n"
        "3. Determine 'risk_profile' by evaluating portfolio volatility and sector concentration.\n"
        "4. OUTPUT: A single valid JSON object only. No markdown, no code blocks.\n"
    )

    def get_content_config(self) -> types.GenerateContentConfig:
        """Returns the content generation configuration for the agent."""
        return types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
            response_mime_type="application/json",
        )
