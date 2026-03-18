from datetime import timezone, datetime
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import json
from app.apis.services.file_service.service import FileService
from app.apis.services.file_service.zeroda import ZerodhaFileService
from app.ai.google_vertex.agents.tools.firestore_datastore import get_latest_analysis
from app.ai.google_vertex.workflows.finadvisory_orchestrator import FinAdvisorOrchestrator
from app.apis.services.queue_service.queue_service_provider import QueueServiceProvider
from app.apis.services.container import container


load_dotenv()  

app = FastAPI()

@app.post("/analyze-portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    """ API to analzs the protfolio data"""
    protfolio_data: dict = FileService().parse_file(ZerodhaFileService(file))
    queue_data: dict = {
        "data": protfolio_data,
        "pushed_at": datetime.now(timezone.utc)
    }
    QueueServiceProvider(container.queue_service).push(queue_data)
    return {
        "status": "success",
        "message": "We are analysing the stocks. You will get email notification once succeeded."
    }


async def process_protfolio(file): 
    """ process the protfolio data """
    try:  
        stocks = FileService().parse_file(container.file_service)
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