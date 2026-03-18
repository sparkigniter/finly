from google.adk import Agent
from app.ai.google_vertex.agents.formatter.schemas.response import PortfolioBreakdown
from typing import Optional
from app.ai.google_vertex.agents.tools.firestore_datastore import store_portfolio_analysis, get_latest_analysis

class DataStoreAgent:
    """
    Agent responsible for storing portfolio analysis data.

    The DataStoreAgent receives structured research data and ensures it is stored
    in the database using the 'store_portfolio_analysis' tool. It validates the data
    against the PortfolioBreakdown schema before storage.
    """

    # Internal singleton instance to prevent redundant memory allocation
    __agent: Optional[Agent] = None

    # System Instruction: Defines the agent's behavior as a data storage specialist.
    instruction =  """### ROLE
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

    def __create_agent() -> Agent:
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
            model="gemini-2.5-flash",
            name="datastore_agent",
            output_key="formatted_data",
            instruction=DataStoreAgent.instruction,
            tools= [store_portfolio_analysis]
        )
        DataStoreAgent.__agent = agent
        return agent

    @staticmethod
    def get_agent() -> Agent:
        """
        Retrieves the persistent singleton instance of the agent.
        Ensures only one instance exists within the current execution context.

        Returns:
            Agent: The singleton agent instance.
        """
        if DataStoreAgent.__agent is None:
            DataStoreAgent.__create_agent()
        return DataStoreAgent.__agent

    @staticmethod
    def get_new_agent() -> Agent:
        """
        Factory method to generate a brand new Agent instance.
        Useful when you need to bypass cached state or isolation.

        Returns:
            Agent: A fresh Agent instance.
        """
        return DataStoreAgent.__create_agent()