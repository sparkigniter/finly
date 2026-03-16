from google.adk import Agent
from App.AI.GoogleVertex.Agents.Formatter.Schemas.Response import PortfolioBreakdown
from typing import Optional

class FormatterAgent:
    """
    Agent responsible for data restructuring and validation.
    
    The FormatterAgent takes unstructured research data and maps it to a strict 
    Pydantic schema (PortfolioBreakdown), ensuring data integrity for the 
    application frontend and database.
    """

    # Internal singleton instance to prevent redundant memory allocation
    __agent: Optional[Agent] = None

    # System Instruction: Defines the agent's behavior as a pure data-mapping specialist.
    instruction =  """### ROLE
            You are a high-precision Data Structuring Agent for the Finly investment platform.

            ### GOAL
            Transform the raw financial analysis provided by the Research Agent into a strictly validated JSON structure.

            ### RULES
            1. DATA EXTRACTION: Extract all stock tickers, sector allocations, and performance metrics.
            2. SCHEMA ADHERENCE: You MUST match the 'PortfolioBreakdown' schema exactly. Do not add keys outside the schema.
            3. OUTPUT: Produce ONLY the JSON object. Do not provide conversational filler or explanations.
            4. CONTINUATION: Once the JSON is generated, it will be stored in the 'formatted_data' key for the DataStoreAgent to persist.
            """
    @staticmethod
    def __create_agent() -> Agent:
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
            model="gemini-2.5-flash",
            name="formatter_agent",
            output_key="formatted_data",
            instruction=FormatterAgent.instruction,
            # Link the Pydantic model to force structured JSON output
            output_schema=PortfolioBreakdown
        )
        FormatterAgent.__agent = agent
        return agent

    @staticmethod
    def get_agent() -> Agent:
        """
        Retrieves the persistent singleton instance of the agent.
        Ensures only one instance exists within the current execution context.

        Returns:
            Agent: The singleton agent instance.
        """
        if FormatterAgent.__agent is None:
            FormatterAgent.__create_agent()
        return FormatterAgent.__agent

    @staticmethod
    def get_new_agent() -> Agent:
        """
        Factory method to generate a brand new Agent instance.
        Useful when you need to bypass cached state or isolation.

        Returns:
            Agent: A fresh Agent instance.
        """
        return FormatterAgent.__create_agent()