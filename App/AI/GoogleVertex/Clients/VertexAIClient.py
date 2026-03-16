import vertexai
import os
from dotenv import load_dotenv
load_dotenv()

class VertexClient:
    @staticmethod
    def init():
       return vertexai.init(
            project= os.getenv("PROJECT_ID"),
            location= os.getenv("REGION"),
            staging_bucket= os.getenv("STAGING_BUCKET")
        )
