from datetime import timezone, datetime
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import json
from app.backend.services.file_service.file_service_provider import FileServiceProvider
from app.backend.services.file_service.zeroda import ZerodhaFileService
from app.ai.google_vertex.agents.tools.firestore_datastore import get_latest_analysis
from app.ai.google_vertex.workflows.finadvisory_orchestrator import FinAdvisorOrchestrator
from app.backend.services.container import container
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()  

app = FastAPI()

# 1. Define the origins that are allowed to talk to your server
origins = [
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",  # Alternative local address
]

# 2. Add the middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allow your React app
    allow_credentials=True,
    allow_methods=["*"],             # Allow GET, POST, etc.
    allow_headers=["*"],             # Allow all headers
)

@app.post("/analyze-portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    """ API to analyze the portfolio data"""
    portfolio_data: dict = await container.file_service.parse_file(file= file)
    queue_data: dict = {
        "data": portfolio_data,
        "pushed_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    container.protfolio_analysis_queue.push(queue_data)
    return {
        "status": "success",
        "message": "We are analysing the stocks. You will get email notification once succeeded."
    }


async def process_portfolio(file): 
    """ process the portfolio data """
    try:  
        stocks = await container.file_service.parse_file(file= file)
        batch_size = 30
        for i in range(0, len(stocks), batch_size):
            batch = stocks[i:i + batch_size]
            print(f"Processing batch: {batch}")
            await FinAdvisorOrchestrator.analyze_portfolio(
                user_id="test",
                file_content=json.dumps(batch))

        return {
            "status": "success",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/portfolio/{user_id}")
async def fetch_ui_data(user_id: str):
    # This directly fetches the JSON string from SQL
    data = get_latest_analysis(user_id)
    json_data = json.loads(data)
    return json_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=3600)