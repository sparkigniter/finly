from fastapi import FastAPI, UploadFile, File, BackgroundTasks
import pandas as pd
import io
import os
from App.AI.GoogleVertex.Agents.FinAdvisory.Agent import FinAdvisorAgent
import json
from App.AI.GoogleVertex.Agents.Tools.FirestoreTools import get_latest_analysis
from App.AI.GoogleVertex.Workflows.Orchestrator import FinAdvisorOrchestrator
import os
from dotenv import load_dotenv
load_dotenv()  

app = FastAPI()


async def parse_zeroda_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    # Load raw sheet without headers
    raw_df = pd.read_excel(io.BytesIO(file_bytes), header=None)

    # Find the row where the table header starts
    header_row = None
    for idx, row in raw_df.iterrows():
        if "Symbol" in row.values:
            header_row = idx
            break

    if header_row is None:
        raise ValueError("Could not locate stock table in Zerodha export")

    # Extract header
    headers = raw_df.iloc[header_row].tolist()

    # Extract table rows
    table_df = raw_df.iloc[header_row + 1:].copy()
    table_df.columns = headers

    # Remove empty rows
    table_df = table_df[table_df["Symbol"].notna()]

    # Select relevant columns
    table_df = table_df[
        [
            "Symbol",
            "Open Quantity",
            "Open Value",
            "Unrealized P&L",
            "Unrealized P&L Pct."
        ]
    ]

    # Rename columns
    table_df = table_df.rename(
        columns={
            "Symbol": "stock",
            "Open Quantity": "quantity",
            "Open Value": "investment",
            "Unrealized P&L": "total_gain_loss",
            "Unrealized P&L Pct.": "performance_pct"
        }
    )

    table_df = table_df.fillna(0)

    return table_df.to_dict(orient="records")


@app.post("/analyze-portfolio")
async def analyze_portfolio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

        background_tasks.add_task(process_protfolio, file)

        return {
            "status": "Analysis the data. Data will be reflected in your accout soon",
        }
    

async def process_protfolio(file) : 

    try:
        stocks_json = await parse_zeroda_file(file)
        batch_size = 30
        for i in range(0, len(stocks_json), batch_size):
            batch = stocks_json[i:i + batch_size]
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