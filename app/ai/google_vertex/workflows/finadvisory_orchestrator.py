"""This module defines the FinAdvisorAgent for protfolio analysis."""
import json
import asyncio
import logging
from datetime import datetime, timezone
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

# --- DEVOPS FIX: STABLE VERTEX AI MODEL IDS ---
# RCA: Using 'gemini-3.1-pro' or 'free-tier' endpoints leads to 429 Limit: 0 errors.
# Fix: Use explicit Vertex AI production models (-002 suffix).
MODEL_HIERARCHY = [
    "gemini-1.5-flash-002",  # Most stable, highest quota, lowest cost
    "gemini-1.5-pro-002",    # Higher intelligence fallback
    "gemini-1.5-flash-8b"    # Ultra-lightweight emergency fallback
]

class FinAdvisorOrchestrator:
    """
    Orchestrator class managing the end-to-end portfolio analysis workflow.
    Fixed 429 Resource Exhausted by switching to Vertex AI Production Models.
    """

    def __init__(self):
        self.fin_advisor_agent = FinAdvisorAgent(config=None)
        self.formatter_agent = FormatterAgent(config=None)

    def get_pipeline(self) -> SequentialAgent:
        return SequentialAgent(
            name="PortfolioPipeline",
            sub_agents=[
                self.fin_advisor_agent.agent(),
                self.formatter_agent.agent(),
            ],
        )

    async def analyze_portfolio(self, user_id: str, portfolio_data: any):
        """
        Executes multi-agent pipeline with payload optimization and 429 retry logic.
        """
        if isinstance(portfolio_data, list):
            holdings = portfolio_data
            pushed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        elif isinstance(portfolio_data, dict):
            holdings = portfolio_data.get("data", [])
            pushed_at = portfolio_data.get("pushed_at", "Unknown")

        logger.info(f"🚀 [DevOps] Starting analysis for {user_id} | Stocks: {len(holdings)}")

        if not holdings:
            raise DataValidationError("Portfolio 'data' key is empty or missing.")

        # Optimization to stay under TPM (Tokens Per Minute) limits
        optimized_data = [
            {
                "symbol": s.get("symbol"),
                "qty": s.get("quantity"),
                "avg_price": s.get("average_price"),
                "ltp": s.get("last_price")
            } for s in holdings
        ]

        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Analyze this portfolio: {json.dumps(optimized_data)}"
                )
            ],
        )

        for model_name in MODEL_HIERARCHY:
            logger.info(f"🛠️ [Attempt] Model: {model_name}")
            
            session_service = InMemorySessionService()
            portfolio_pipeline = self.get_pipeline()
            
            if hasattr(self.fin_advisor_agent, 'update_model'):
                self.fin_advisor_agent.update_model(model_name)

            runner = Runner(
                agent=portfolio_pipeline,
                session_service=session_service,
                app_name="FinApp"
            )

            try:
                session = await session_service.create_session(
                    app_name="FinApp", user_id=user_id, state={"user_id": user_id}
                )

                final_response_received = False
                
                async with asyncio.timeout(90):
                    async for event in runner.run_async(
                        new_message=user_message, 
                        session_id=session.id, 
                        user_id=user_id
                    ):
                        if event.is_final_response():
                            final_response_received = True

                if not final_response_received:
                    raise PortfolioAnalysisError("Pipeline closed without final_response")

                session_state = await session_service.get_session(
                    app_name="FinApp", user_id=user_id, session_id=session.id
                )

                formatted_data = session_state.state.get("formatted_data")
                if not formatted_data:
                    raise PortfolioAnalysisError("formatted_data missing from state")

                store_portfolio_analysis(formatted_data, session_state)
                return formatted_data

            except Exception as e:
                err_msg = str(e).upper()
                
                # Check for the specific 429/RESOURCE_EXHAUSTED/QUOTA error
                if any(x in err_msg for x in ["429", "RESOURCE_EXHAUSTED", "QUOTA"]):
                    logger.warning(f"⚠️ Quota exceeded for {model_name}. Retrying with fallback...")
                    # Small backoff before trying the next model in hierarchy
                    await asyncio.sleep(2)
                    if model_name != MODEL_HIERARCHY[-1]:
                        continue 
                    else:
                        raise RateLimitError("Critical: All Vertex AI quotas exhausted. Check Billing.")
                
                raise PortfolioAnalysisError(f"Analysis failed: {str(e)}")

        return None