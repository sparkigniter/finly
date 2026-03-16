from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

from App.AI.GoogleVertex.Workflows.Orchestrator import FinAdvisorOrchestrator
from App.AI.GoogleVertex.Clients.VertexAIClient import VertexClient

def create() -> None:
    """
    Deploys the Financial Advisor agent pipeline to Vertex AI Agent Engine.
    
    This function initializes the Vertex client, constructs the agent hierarchy,
    and pushes the configuration to the cloud with all necessary dependencies.
    """

    # 1. Initialize Vertex AI (Project, Location, Staging Bucket)
    VertexClient.init()

    # 2. Retrieve the Root Pipeline (The SequentialAgent containing Researcher & Formatter)
    root_agent = FinAdvisorOrchestrator.get_pipeline()
    
    # 3. Wrap in AdkApp to enable cloud-specific features like Tracing
    adk_app = AdkApp(agent=root_agent, enable_tracing=True)

    # 4. Deploy to the Reasoning Engine
    remote_agent = agent_engines.create(
        adk_app,
        display_name=root_agent.name,
        requirements=[
            "google-cloud-aiplatform[agent_engines]==1.141.0",
            "google-cloud-firestore==2.10.0",
            "pandas==3.0.1",
            "protobuf>=6.0.0,<7.0.0",
            "pydantic==2.12.5",
            "python-dotenv==1.2.2",
            "google-adk>=0.0.2",
            "google-genai>=1.5.0"
        ],
        # CRITICAL: This zips up your 'App' folder so imports like 
        # 'App.AI.GoogleVertex...' work in the cloud environment.
        extra_packages=["./App"], 
    )

    print(f"✅ Created remote agent: {remote_agent.resource_name}")

if __name__ == "__main__":
    create()