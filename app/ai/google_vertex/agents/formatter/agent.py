"""Agent responsible for data restructuring and validation."""
from typing import Optional
from google.adk import Agent
from app.ai.google_vertex.agents.formatter.schemas.response import PortfolioBreakdown
from app.ai.google_vertex.agents.formatter.config import FormatterConfig


class FormatterAgent:
    """
    Agent responsible for data restructuring and validation.

    The FormatterAgent takes unstructured research data and maps it to a strict
    Pydantic schema (PortfolioBreakdown), ensuring data integrity for the
    application frontend and database.
    """

    # Internal singleton instance to prevent redundant memory allocation
    _agent: Optional[Agent] = None
    config: Optional[FormatterConfig] = None
    _model: str = "gemini-2.5-flash"
    _name: str = "formatter_agent"

    def __init__(self, config: Optional[FormatterConfig]):
        self.config = config or FormatterConfig()
        self._create_agent()

    def _create_agent(self) -> Agent:
        """
        Initializes a fresh Agent instance with strict schema constraints.

        Configures the agent with:
        - Model: Gemini 2.5 Flash (optimized for structured data generation).
        - Output Key: 'formatted_data' (used for session state lookup).
        - Output Schema: PortfolioBreakdown (Pydantic-based validation).

        Returns:
            Agent: The configured ADK Agent instance.
        """
        agent = Agent(
            model=self._model,
            name=self._name,
            output_key="formatted_data",
            instruction=self.config.instruction,
            generate_content_config=self.config.get_content_config(),
            output_schema=PortfolioBreakdown,
        )
        FormatterAgent._agent = agent
        return agent

    def agent(self) -> Agent:
        """Provides access to the Agent instance."""
        return FormatterAgent._agent
