from email.mime import message
from zipfile import Path
from google.adk import Agent
from vertexai import agent_engines
from google.adk.tools import google_search_tool
from pathlib import Path
from App.AI.GoogleVertex.Agents.Formatter.Schemas.Response import PortfolioBreakdown

class FormatterAgent:

    __agent = None
    instruction = f"""Take the raw data given and convert it strictly into the required JSON format. Ensure all fields like performance_pct and recommendation are correctly mapped."""

    @staticmethod
    def __create_agent():
        # Define the core agent
        search_tool = google_search_tool.GoogleSearchTool()
        agent = Agent(
            model="gemini-2.5-flash",
            name='formatter_agent',
            output_key='formatted_portfolio_data',
            instruction= FormatterAgent.instruction,
            output_schema=PortfolioBreakdown
        )
        # Wrap it in the AdkApp for Vertex AI integration
        FormatterAgent.__agent = agent
        return agent
    
    @staticmethod
    def get_agent():
        if FormatterAgent.__agent is None:
            FormatterAgent.__create_agent()
        return FormatterAgent.__agent
    
    @staticmethod
    def get_new_agent():
        return FormatterAgent.__create_agent()