from App.AI.GoogleVertex.Agents.FinAdvisory.Agent import FinAdvisorAgent
from App.AI.GoogleVertex.Agents.Formatter.Agent import FormatterAgent
from google.adk.agents import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

class FinAdvisorOrchestrator:

    @staticmethod
    async def analyze_portfolio(user_id, file_content):

        session_service = InMemorySessionService()
        FinAdvisorAgent.append_instruction(f"TASK: Analyze ONLY the stocks provided in: {file_content}.")
        portfolio_pipeline = SequentialAgent(
            name="PortfolioPipeline",
            sub_agents=[
                FinAdvisorAgent.get_new_agent(),
                FormatterAgent.get_new_agent()
            ]
        )
        runner = Runner(agent=portfolio_pipeline, session_service=session_service, app_name="FinApp")
        session = await session_service.create_session(
            app_name="FinApp",
            user_id="user_123"
        )
        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text = f"Analyze the stocks : {file_content}.")]
        )
        print("file content in orchestrator:", file_content )
        async for event in runner.run_async(new_message=user_message, session_id=session.id, user_id="user_123"):
            if event.is_final_response():
                # This will be your validated PortfolioBreakdown object
                print(event.content.parts[0].text)
                return event.content.parts[0].text  # Return the final formatted portfolio data as JSON string
        return None
