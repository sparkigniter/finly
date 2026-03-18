from google.adk.agents import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.google_vertex.agents.finadvisory.agent import FinAdvisorAgent
from app.ai.google_vertex.agents.formatter.agent import FormatterAgent
from app.ai.google_vertex.agents.datastore.agent import DataStoreAgent

class FinAdvisorOrchestrator:
    """
    Orchestrator class responsible for managing the end-to-end portfolio analysis workflow.
    """

    @staticmethod
    def get_pipeline() -> SequentialAgent:
        """
        Constructs and returns the core agent pipeline hierarchy.
        This method is essential for deployment to Vertex AI Agent Engine.

        Returns:
            SequentialAgent: The orchestrator's root agent containing sub-agents.
        """
        print("[FinAdvisorOrchestrator] Creating new pipeline with FinAdvisorAgent and FormatterAgent")

        FinAdvisorAgent.set_temperature(0.1)
        FinAdvisorAgent.set_max_output_tokens(100000)

        # We use fresh instances to avoid parent_agent assignment errors
        return SequentialAgent(
            name="PortfolioPipeline",
            sub_agents=[
                FinAdvisorAgent.get_new_agent(),
                FormatterAgent.get_new_agent(),
                DataStoreAgent.get_new_agent()
            ]
        )

    @staticmethod
    async def analyze_portfolio(user_id: str, file_content: list):
        """
        Executes the sequential multi-agent pipeline to analyze stock data.

        Args:
            user_id (str): Unique identifier for the user session.
            file_content (list): A list of stock dictionaries.
        """
        print(f"[analyze_portfolio] Starting analysis for user_id: {user_id}")
        session_service = InMemorySessionService()

        # Update grounding instructions
        print(f"[analyze_portfolio] Appending instruction for stocks: {file_content}")
        FinAdvisorAgent.append_instruction(
            f"TASK: Analyze ONLY the stocks provided in: {file_content}."
        )

        # Retrieve the pipeline from the new helper method
        print("[analyze_portfolio] Retrieving pipeline")
        portfolio_pipeline = FinAdvisorOrchestrator.get_pipeline()

        # Initialize the Runner
        print("[analyze_portfolio] Initializing Runner")
        runner = Runner(
            agent=portfolio_pipeline,
            session_service=session_service,
            app_name="FinApp"
        )

        # Create a unique session
        print("[analyze_portfolio] Creating session")
        session = await session_service.create_session(
            app_name="FinApp",
            user_id=user_id
        )

        # Prepare the user message
        print("[analyze_portfolio] Preparing user message")
        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=f"Analyze the stocks: {file_content}.")]
        )

        # Execution loop
        print("[analyze_portfolio] Starting execution loop")
        async for event in runner.run_async(
            new_message=user_message,
            session_id=session.id,
            user_id=user_id
        ):
            if event.is_final_response():
                final_json = event.content.parts[0].text
                print(f"[analyze_portfolio] Final response: {final_json}")

        print("[analyze_portfolio] No final response received")
        return None