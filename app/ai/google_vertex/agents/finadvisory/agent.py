from google.adk import Agent
from google.adk.tools import google_search_tool
from pathlib import Path
from typing import Optional
from google.genai import types


class FinAdvisorAgent:
    """
    A specialized financial advisor agent designed to process Zerodha broker exports.
    
    This class serves as a factory for creating and managing a Google ADK Agent
    tailored for portfolio analysis, news grounding, and JSON-structured reporting.
    """

    # Internal singleton instance of the ADK Agent
    __agent: Optional[Agent] = None

    __temperature = 0.9

    __max_output_tokens = 1000

    __top_p = 0.95

    # System instruction: Defines the agent's persona, tool-usage logic, 
    # and strict output constraints for financial analysis.
    instruction = """As a financial advisor, analyze the uploaded Zerodha broker export. 
            1. Calculate gains/losses using code_execution.
            2. Search for the latest news/dividends for each ticker.
            3. Give recommendations based on the analysis and the reasons. (e.g., "Hold", "Sell", "Buy More")
            4. Give the technical indicator and fundamental indicator trends for each stock.
            5. Return the results in the exact JSON schema provided.
            
        IMPORTANT: Ensure you analyze each stock's performance and give a recommendation for each. 
        DO NOT add additional stocks which are not provided. Use google_search for news 
        and code_execution for calculations. Strictly adhere to the provided JSON schema."""

    @staticmethod
    def __create_agent() -> Agent:
        """
        Private factory method to initialize the ADK Agent instance.
        
        Configures the agent with:
        - Model: Gemini 2.5 Flash (for high-speed financial processing)
        - Tools: Google Search (for market grounding)
        - Output Key: 'formatted_data' (for state persistence)
        
        Returns:
            Agent: A fully configured Google ADK Agent instance.
        """
        # Initialize market-grounding tools
        search_tool = google_search_tool.GoogleSearchTool()
        
        agent = Agent(
            model="gemini-2.5-flash",
            name='financial_advisor_agent',
            output_key='formatted_data',
            tools=[search_tool],
            instruction=FinAdvisorAgent.instruction,
            generate_content_config= FinAdvisorAgent.get_content_config()
        )
        
        # Cache the agent instance for singleton behavior
        FinAdvisorAgent.__agent = agent
        return agent
    
    @staticmethod
    def get_agent() -> Agent:
        """
        Retrieves the singleton instance of the agent. 
        If it doesn't exist, it triggers the creation process.
        
        Returns:
            Agent: The cached or newly created financial advisor agent.
        """
        if FinAdvisorAgent.__agent is None:
            FinAdvisorAgent.__create_agent()
        return FinAdvisorAgent.__agent
    
    @staticmethod
    def get_new_agent() -> Agent:
        """
        Forces the creation of a fresh agent instance. 
        Useful for resetting conversation state or changing configurations.
        
        Returns:
            Agent: A brand new ADK Agent instance.
        """
        return FinAdvisorAgent.__create_agent()
    
    @staticmethod
    def append_instruction(additional_instruction: str) -> None:
        """
        Extends the base system instruction with additional context or user constraints.
        
        Args:
            additional_instruction (str): Text to be appended to the current instruction.
        """
        FinAdvisorAgent.instruction += " " + additional_instruction
    
    def set_temperature(temperature: int) -> None:
        FinAdvisorAgent.__temperature = temperature

    def get_temperature() -> int: 
        return FinAdvisorAgent.__temperature
    
    def set_max_output_tokens(max_output_tokens: int) -> None:
        FinAdvisorAgent.__max_output_tokens = max_output_tokens

    def get_max_output_tokens() -> int:
        return FinAdvisorAgent.__max_output_tokens

    def set_top_p(top_p: int) -> None:
        FinAdvisorAgent.__top_p = top_p

    def get_top_p() -> int:
        return FinAdvisorAgent.__top_p
    
    def get_content_config() -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            temperature= FinAdvisorAgent.get_temperature(),
            max_output_tokens= FinAdvisorAgent.get_max_output_tokens(),
            top_p= FinAdvisorAgent.get_top_p()
        )