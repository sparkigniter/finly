"""This module defines the FinAdvisorAgent for portfolio analysis."""
import json
import asyncio
from datetime import datetime, timezone
import re
from google.adk.agents import SequentialAgent
from google.adk.runners import Runner, logger
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.google_vertex.agents.tools.firestore_datastore import (
    patch_portfolio_analysis,
    get_stocks
)
from app.ai.google_vertex.agents.finadvisory.stocks.agent import FinAdvisorStocksAgent
from app.ai.google_vertex.agents.finadvisory.protfolio.agent import FinAdvisorProtfolioAgent
from app.ai.google_vertex.agents.formatter.agent import FormatterAgent
from app.backend.queues.stocks_process import StockProcessQueue
from app.ai.google_vertex.agents.formatter.schemas.stock import StockAnalysisResponse
from app.ai.google_vertex.agents.formatter.schemas.protfolio import PortfolioAnalysisResponse

from app.ai.errors.error import (
    PortfolioAnalysisError,
    DataValidationError,
)

class FinAdvisorOrchestrator:
    """
    Orchestrator class managing the end-to-end portfolio analysis workflow.
    
    This class:
    - Validates portfolio data
    - Runs the analysis pipeline
    - Stores results when final response is received
    - Returns JSON response
    """

    def get_pipeline(self, parent_agent, output_schema: any) -> SequentialAgent:
        """
        Create the sequential agent pipeline.
        
        Returns:
            SequentialAgent: Pipeline with FinAdvisor and Formatter agents
        """
        return SequentialAgent(
            name="PortfolioPipeline",
            parent_agent= parent_agent,
            sub_agents=[
                FormatterAgent(config=None, output_schema=output_schema).agent(),
            ],
        )

    async def analyze_stocks(self, user_id: str, stocks_data: dict) -> dict:
        """
        Executes the portfolio analysis pipeline and stores results.
        
        Args:
            user_id: Unique user identifier
            portfolio_data: Portfolio data (dict or list of holdings)
            
        Returns:
            dict: JSON response containing portfolio analysis
            
        Raises:
            DataValidationError: If portfolio data is invalid
            PortfolioAnalysisError: If analysis pipeline fails
        """
        
        
        logger.info(
            f"🚀 Starting stocks analysis for user: {user_id} | "
            f"Holdings count: {len(stocks_data)} | Pushed at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )

        # Validate holdings are not empty
        if not stocks_data:
            raise DataValidationError(
                "stocks_data 'data' is empty or missing. "
                "Please provide at least one holding."
            )
        
        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Analyze this portfolio: {json.dumps(stocks_data)}"
                )
            ],
        )
        session_service = InMemorySessionService()
        portfolio_pipeline = self.get_pipeline(FinAdvisorStocksAgent().agent(), output_schema=StockAnalysisResponse)

        runner = Runner(
            agent=portfolio_pipeline,
            session_service=session_service,
            app_name="FinApp"
        )

        try:
            session = await session_service.create_session(
                app_name="FinApp",
                user_id=user_id,
                state={"user_id": user_id}
            )
            logger.info(f"Session created: {session.id}")
            print("[analyze_stocks] Starting execution loop")
            MAX_RETRIES = 3
            MAX_DELAY = 30
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    async for event in runner.run_async(
                        new_message=user_message,
                        session_id=session.id,
                        user_id=user_id
                    ):
                        print(f"[analyze_stocks] Received event: {event}")
                        if event.is_final_response():
                            print(f"[analyze_stocks] Final response received.")
                            break
                    break
                except Exception as e:
                    logger.error(f"Attempt {attempt} failed: {str(e)}")
                    if attempt == MAX_RETRIES:
                        raise PortfolioAnalysisError(
                            f"Portfolio analysis failed after {MAX_RETRIES} attempts: {str(e)}"
                        ) from e
                    delay = min(2 ** attempt, MAX_DELAY)
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)

            session_state = await session_service.get_session(
                app_name="FinApp",
                user_id=user_id,
                session_id=session.id
            )

            formatted_data = session_state.state.get("formatted_data")

            if not formatted_data:
                print("[analyze_portfolio] Warning: formatted_data not found in session state")
                return None

            print(f"[analyze_portfolio] Final JSON: {formatted_data}")
            patch_portfolio_analysis(user_id=user_id, stock_insights=formatted_data.get('stocks'), protfolio_insights=None )
            return formatted_data
        except Exception as e: 
            logger.error(f"Portfolio analysis failed: {str(e)}")
            raise PortfolioAnalysisError(f"Portfolio analysis failed: {str(e)}") from e

    async def analyze_protfolio(self, user_id: str, protfolio_data: dict) -> dict:
        """
        Executes the portfolio analysis pipeline and stores results.
        
        Args:
            user_id: Unique user identifier
            portfolio_data: Portfolio data (dict or list of holdings)
            
        Returns:
            dict: JSON response containing portfolio analysis
            
        Raises:
            DataValidationError: If portfolio data is invalid
            PortfolioAnalysisError: If analysis pipeline fails
        """
        
        logger.info(
            f"🚀 Starting protfolio analysis for user: {user_id} |  Pushed at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )

        # Validate holdings are not empty
        if not protfolio_data:
            raise DataValidationError(
                "stocks_data 'data' is empty or missing. "
                "Please provide at least one holding."
            )
        
        print(f"[analyze_protfolio] protfolio_data: {protfolio_data}")
        
        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Analyze this portfolio: {json.dumps(protfolio_data)}"
                )
            ],
        )
        session_service = InMemorySessionService()
        portfolio_pipeline = self.get_pipeline(FinAdvisorProtfolioAgent().agent(), output_schema=PortfolioAnalysisResponse)

        runner = Runner(
            agent=portfolio_pipeline,
            session_service=session_service,
            app_name="FinApp"
        )

        try:
            # Create session
            session = await session_service.create_session(
                app_name="FinApp",
                user_id=user_id,
                state={"user_id": user_id}
            )

            logger.info(f"Session created: {session.id}")
                    # Execution loop
            print("[analyze_stocks] Starting execution loop")
            MAX_RETRIES = 3
            MAX_DELAY = 30
            for attempt in range(1, MAX_RETRIES + 1): 
                try:
                    async for event in runner.run_async(
                        new_message=user_message,
                        session_id=session.id,
                        user_id=user_id
                    ):
                        print(f"[analyze_stocks] Received event: {event}")
                        if event.is_final_response():
                            print(f"[analyze_stocks] Final response received")
                            print(event.content)
                            break
                    break  # Exit retry loop if successful
                except Exception as e:
                    logger.error(f"Attempt {attempt} failed: {str(e)}")
                    if attempt == MAX_RETRIES:
                        raise PortfolioAnalysisError(
                            f"Portfolio analysis failed after {MAX_RETRIES} attempts: {str(e)}"
                        ) from e
                    delay = min(2 ** attempt, MAX_DELAY)
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)

            session_state = await session_service.get_session(
                app_name="FinApp",
                user_id=user_id,
                session_id=session.id
            )

            formatted_data = session_state.state.get("formatted_data")

            if not formatted_data:
                print("[analyze_portfolio] Warning: formatted_data not found in session state")
                return None

            print(f"[analyze_portfolio] Final JSON: {formatted_data}")
            patch_portfolio_analysis(user_id=user_id, stock_insights=None, protfolio_insights=formatted_data.get('portfolio_insights'))
            return formatted_data
        except Exception as e: 
            logger.error(f"Portfolio analysis failed: {str(e)}")
            raise PortfolioAnalysisError(f"Portfolio analysis failed: {str(e)}") from e
