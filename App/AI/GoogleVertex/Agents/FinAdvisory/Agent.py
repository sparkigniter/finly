from email.mime import message
from zipfile import Path
from google.adk import Agent
from vertexai import agent_engines
from google.adk.tools import google_search_tool
from pathlib import Path

class FinAdvisorAgent:

    __agent = None
    instruction = f"""As a financial advisor, analyze the uploaded Zerodha broker export. 
            1. Calculate gains/losses using code_execution.
            2. Search for the latest news/dividends for each ticker.
            3. Give recommendations based on the analysis and the reasons. (e.g., "Hold", "Sell", "Buy More")
            4. Give the technical indicator and fundamental indicator trends for each stock (e.g., "RSI is above 70, indicating overbought conditions", "P/E ratio is below industry average, indicating undervaluation").
            5. Return the results in the exact JSON schema provided.
        Impratly, enusure you analyze each stocks performance and give a recommendation for each stock. Also, make sure you don't add any additional stocks which are not given to you to analyze. The recommendation should be based on the performance of the stock, the latest news, and the technical/fundamental indicators.
        Import the latest news using google_search tool with the query "<ticker> stock news latest" for each ticker in the portfolio. Use code_execution tool to calculate gains/losses based on the transaction history in the Zerodha export. Ensure the final output strictly adheres to the provided JSON schema, including all required fields and correct data types."""

    @staticmethod
    def __create_agent():
        # Define the core agent
        search_tool = google_search_tool.GoogleSearchTool()
        agent = Agent(
            model="gemini-2.5-flash",
            name='financial_advisor_agent',
            output_key='portfolio_analysis_data',
            tools=[search_tool],  
            instruction= FinAdvisorAgent.instruction
        )
        # Wrap it in the AdkApp for Vertex AI integration
        FinAdvisorAgent.__agent = agent
        return agent
    
    @staticmethod
    def get_agent():
        if FinAdvisorAgent.__agent is None:
            FinAdvisorAgent.__create_agent()
        return FinAdvisorAgent.__agent
    
    @staticmethod
    def get_new_agent():
        return FinAdvisorAgent.__create_agent()
    
    @staticmethod
    def append_instruction(additional_instruction):
        FinAdvisorAgent.instruction += " " + additional_instruction
