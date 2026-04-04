"""Orchestrator for the financial advisory workflow using Google Vertex AI."""

import json
import asyncio
from google.adk.agents import SequentialAgent
from google.adk.runners import Runner, logger
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.google_vertex.agents.tools.firestore_datastore import (
    store_portfolio_analysis,
)
from app.ai.google_vertex.agents.finadvisory.agent import FinAdvisorAgent
from app.ai.google_vertex.agents.formatter.agent import FormatterAgent
from app.ai.errors.error import (
    PortfolioAnalysisError,
    RateLimitError,
    DataValidationError,
)


class FinAdvisorOrchestrator:
    """
    Orchestrator class responsible for managing the end-to-end portfolio analysis workflow.
    """

    def __init__(self):
        self.fin_advisor_agent = FinAdvisorAgent(config=None)
        self.formatter_agent = FormatterAgent(config=None)
        # self.data_store_agent = DataStoreAgent(config=None)

    def get_pipeline(self) -> SequentialAgent:
        """
        Constructs and returns the core agent pipeline hierarchy.
        This method is essential for deployment to Vertex AI Agent Engine.

        Returns:
            SequentialAgent: The orchestrator's root agent containing sub-agents.
        """
        print(
            "[FinAdvisorOrchestrator] Creating new pipeline with FinAdvisorAgent and FormatterAgent"
        )

        # We use fresh instances to avoid parent_agent assignment errors
        return SequentialAgent(
            name="PortfolioPipeline",
            sub_agents=[
                self.fin_advisor_agent.agent(),
                self.formatter_agent.agent(),
                # self.data_store_agent.agent(),
            ],
        )

    async def analyze_portfolio(self, user_id: str, portfolio_data: list):
        """
        Executes multi-agent pipeline. Throws exceptions for parent handling.
        Implements Exponential Backoff for RESOURCE_EXHAUSTED errors.
        """
        logger.info(f"Starting analysis for user_id: {user_id}")

        if not portfolio_data:
            raise ValueError("Portfolio data cannot be empty")

        max_retries = 3
        retry_delay = 2  # Seconds

        session_service = InMemorySessionService()
        portfolio_pipeline = self.get_pipeline()

        runner = Runner(
            agent=portfolio_pipeline,
            session_service=session_service,
            app_name="FinApp")

        session = await session_service.create_session(
            app_name="FinApp", user_id=user_id, state={"user_id": user_id}
        )

        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Analyze the stocks: {json.dumps(portfolio_data)}"
                )
            ],
        )

        for attempt in range(max_retries):
            try:
                async for event in runner.run_async(
                    new_message=user_message, session_id=session.id, user_id=user_id
                ):
                    if event.is_final_response():
                        logger.info(
                            f"Final response event captured for {user_id}")

                session_state = await session_service.get_session(
                    app_name="FinApp", user_id=user_id, session_id=session.id
                )

                formatted_data = session_state.state.get("formatted_data")

                if not formatted_data:
                    raise PortfolioAnalysisError(
                        "Pipeline finished but 'formatted_data' missing from state"
                    )

                # Persist and Return
                store_portfolio_analysis(formatted_data, session_state)
                return formatted_data

            except Exception as e:
                err_msg = str(e).upper()
                if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2**attempt)
                        logger.warning(
                            f"Rate limited (RESOURCE_EXHAUSTED). Retrying in {wait_time}s... (Attempt {attempt + 1})"
                        )
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError(
                            "AI Provider quota exhausted after multiple retries"
                        )

                # Handle JSON Failures
                if isinstance(e, json.JSONDecodeError):
                    raise DataValidationError(
                        f"Agent returned unparseable JSON: {str(e)}"
                    )

                # Re-throw unexpected errors for parent logic
                logger.error(
                    f"Critical failure in analyze_portfolio: {str(e)}",
                    exc_info=True)
                raise PortfolioAnalysisError(f"Analysis failed: {str(e)}")
