"""This agent is responsible for storing portfolio analysis data in the database."""

from typing import Optional
from google.adk import Agent
from app.ai.google_vertex.agents.formatter.schemas.response import PortfolioBreakdown
from app.ai.google_vertex.agents.tools.firestore_datastore import (
    store_portfolio_analysis,
)
from app.ai.google_vertex.agents.datastore.config import DataStoreConfig


class DataStoreAgent:
    """
    Agent responsible for storing portfolio analysis data.

    The DataStoreAgent receives structured research data and ensures it is stored
    in the database using the 'store_portfolio_analysis' tool. It validates the data
    against the PortfolioBreakdown schema before storage.
    """

    # Internal singleton instance to prevent redundant memory allocation
    _agent: Optional[Agent] = None
    _model: str = "gemini-2.5-flash"
    _name: str = "datastore_agent"
    config: Optional[DataStoreConfig] = None

    def __init__(self, config: Optional[DataStoreConfig]):
        """Initializes a new instance of the class."""
        self.config = config or DataStoreConfig()
        self._create_agent()

    def _create_agent(self) -> Agent:
        """
        Initializes a fresh Agent instance for storing portfolio analysis data.

        Configures the agent with:
        - Model: Gemini 2.5 Flash (optimized for structured data handling).
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
            tools=[store_portfolio_analysis],
        )
        DataStoreAgent._agent = agent
        return agent

    def agent(self) -> Agent:
        """Provides access to the Agent instance."""
        return DataStoreAgent._agent
