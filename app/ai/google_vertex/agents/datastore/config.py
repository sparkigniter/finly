"""Configuration settings for the DataStore Agent."""
from google.genai import types


class DataStoreConfig:
    """
    Configuration settings for the DataStore Agent.
    """

    temperature: float = 0.9
    max_output_tokens: int = 1000
    top_p: float = 0.95

    instruction: str = """### ROLE
            You are a Database Execution Agent.

            ### TASK
            1. Access the JSON data stored in the 'formatted_data' key from the previous step.
            2. YOU MUST call the 'store_portfolio_analysis' tool using this data as the input.
            3. DO NOT finish the task or provide a final response until the tool returns a 'Success' message.
            4. If the tool fails, report the specific error.

            ### CONSTRAINTS
            - Do not summarize the data.
            - Do not change the JSON structure.
            - Your only goal is the successful execution of the 'store_portfolio_analysis' tool."""

    def get_content_config(self) -> types.GenerateContentConfig:
        """Returns the content generation configuration for the agent."""
        return types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
        )
