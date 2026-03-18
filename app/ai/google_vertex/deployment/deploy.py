from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

from app.ai.google_vertex.workflows.finadvisory_orchestrator import FinAdvisorOrchestrator
from app.ai.google_vertex.clients.vertext_client import VertexClient


def create() -> None:
    # 1. Clean up existing agents with the same name to avoid duplicates
    display_name = "PortfolioPipeline"  # Matches your root_agent.name
    
    print(f"🔍 Checking for existing agents named '{display_name}'...")
    existing_agents = agent_engines.list(filter=f'display_name="{display_name}"')
    
    for existing in existing_agents:
        print(f"🗑️ Deleting old agent version: {existing.resource_name}")
        # force=True deletes associated sessions/metadata as well
        existing.delete(force=True)

    # 2. Retrieve the Root Pipeline
    root_agent = FinAdvisorOrchestrator.get_pipeline()
    
    # 3. Wrap in AdkApp
    adk_app = AdkApp(agent=root_agent, enable_tracing=True)

    # 4. Deploy (using your corrected requirements)
    print(f"🚀 Deploying new version of '{display_name}'...")
    remote_agent = agent_engines.create(
        adk_app,
        display_name=display_name,
        requirements=[
            "google-cloud-aiplatform[agent_engines]==1.141.0",
            "google-cloud-firestore>=2.25.0", # Fixes the Protobuf conflict
            "pandas==3.0.1",
            "protobuf>=6.0.0,<7.0.0",
            "pydantic==2.12.5",
            "python-dotenv==1.2.2",
            "google-adk>=0.0.2",
            "google-genai>=1.5.0"
        ],
        extra_packages=["./App"], 
    )

    print(f"✅ Created remote agent: {remote_agent.resource_name}")

def delete(resource_id: str) -> None:
    remote_agent = agent_engines.get(resource_id)
    remote_agent.delete(force=True)
    print(f"Deleted remote agent: {resource_id}")


if __name__ == "__main__":
        # 1. Initialize Vertex AI (Project, Location, Staging Bucket)
    VertexClient.init()
    create()