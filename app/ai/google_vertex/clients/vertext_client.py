"""Client for initializing connection to Google Vertex AI."""

import os
import vertexai
from google.auth import default

from dotenv import load_dotenv

load_dotenv()


class VertexClient:
    """Client class for initializing Google Vertex AI connection."""

    @staticmethod
    def init():
        """
        Initializes the Vertex AI client.
        RCA: 401 error occurs because the SDK picks up GOOGLE_API_KEY.
        ValueError occurs because Agent Engine requires a staging_bucket for deployment.
        """
        project_id = os.getenv("PROJECT_ID", "massive-mantra-125114")
        location = os.getenv("REGION", "asia-south1")

        staging_bucket = os.getenv("STAGING_BUCKET")

        if not staging_bucket:
            # Fallback to the known bucket if env is missing to prevent crash
            staging_bucket = "gs://finly-staging-bucket"
            print(
                f"⚠️ Warning: STAGING_BUCKET env var not found. Falling back to: {staging_bucket}"
            )

        # Force the SDK to find your local gcloud credentials
        credentials, _ = default()

        print(
            f"🛠️ Initializing Vertex AI for Project: {project_id} in {location}")
        print(f"📦 Staging Bucket: {staging_bucket}")

        vertexai.init(
            project=project_id,
            location=location,
            credentials=credentials,
            staging_bucket=staging_bucket,
        )
        return credentials
