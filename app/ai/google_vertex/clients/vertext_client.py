"""Client for initializing connection to Google Vertex AI."""
import os
import vertexai
from dotenv import load_dotenv

load_dotenv()


class VertexClient:
    """Client class for initializing Google Vertex AI connection."""
    @staticmethod
    def init():
        """Initializes the Vertex AI client with project and location settings."""
        return vertexai.init(
            project=os.getenv("PROJECT_ID"),
            location=os.getenv("REGION"),
            staging_bucket=os.getenv("STAGING_BUCKET"),
        )
