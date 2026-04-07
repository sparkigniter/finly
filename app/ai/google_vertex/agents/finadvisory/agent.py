"""This module defines the FinAdvisorAgent for protfolio analysis."""

from typing import Optional
from google.adk import Agent
from google.adk.tools import google_search_tool
from app.ai.google_vertex.agents.finadvisory.config import FinAdvisorConfig


class FinAdvisorAgent:
    """
    A specialized financial advisor agent designed to process Zerodha broker exports.

    This class serves as a factory for creating and managing a Google ADK Agent
    tailored for portfolio analysis, news grounding, and JSON-structured reporting.
    """

    _model: str = "gemini-2.5-flash"
    _agent: Optional[Agent] = None
    _name: str = "financial_advisor_agent"
    config: Optional[FinAdvisorConfig] = None

    def __init__(self, config: Optional[FinAdvisorConfig] = None):
        self.config = config or FinAdvisorConfig()
        self._create_agent()

    def _create_agent(self) -> Agent:
        """
        Private factory method to initialize the ADK Agent instance.

        Configures the agent with:
        - Model: Gemini 2.5 Flash (for high-speed financial processing)
        - tools: Google Search (for market grounding)
        - Output Key: 'formatted_data' (for state persistence)

        Returns:
            Agent: A fully configured Google ADK Agent instance.
        """
        # Initialize market-grounding tools
        search_tool = google_search_tool.GoogleSearchTool()

        agent = Agent(
            model=self._model,
            name=self._name,
            output_key="formatted_data",
            tools=[search_tool],
            static_instruction=self.config.instruction,
            generate_content_config=self.config.get_content_config(),
        )
        FinAdvisorAgent._agent = agent
        return agent

    def agent(self) -> Agent:
        """Provides access to the Agent instance."""
        return FinAdvisorAgent._agent

    def instruction(self, instruction: str):
        """Dynamically updates the agent's instruction."""
        self._agent.instruction = instruction

    def update_model(self, model: str):
        """Dynamically updates the agent's model."""
        self._agent.model = model
