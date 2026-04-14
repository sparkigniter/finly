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
        "Strictly map input to the PortfolioAPIResponse JSON schema.\n"
        "Return ONLY valid JSON. No explanations, no markdown, no extra text.\n"
        "Follow schema exactly — no missing or extra fields.\n"
        "Ensure correct data types (int, float, string, null).\n"
        "If any value is missing, use defaults:\n"
        "- numbers: 0\n"
        "- strings: \"\"\n"
        "- lists: []\n"
        "- optional fields: null\n"
        "recommendation must be one of: BUY, HOLD, SELL, STRONG_BUY.\n"
        "Do NOT hallucinate unknown fields or values.\n"
        "Ensure JSON is valid and parsable (no trailing commas)."
    )

    def get_content_config(self) -> types.GenerateContentConfig:
        """Returns the content generation configuration for the agent."""
        return types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
            response_mime_type="application/json",
        )
