import os
from google.cloud import firestore
from datetime import datetime
from google.adk.tools import ToolContext

# Initialize the Firestore client
# It will use the project ID from your environment or VertexAIClient.init()
db = firestore.Client(database="finly")

def store_portfolio_analysis(analysis_data: str, context: ToolContext) -> str:
    """Stores the stock analysis results into Firestore under the user's history."""

    user_id = "testid"
    print(f"[INFO] Storing portfolio analysis for user_id: {user_id}")
    # Reference a collection named 'portfolio_history'
    doc_ref = db.collection("portfolio_history").document()
    #user_id = context.state.get("user_id", "default_user")
    
    
    data = {
        "user_id": user_id,
        "analysis_data": analysis_data,
        "created_at": firestore.SERVER_TIMESTAMP
    }
    
    doc_ref.set(data)
    print(f"[SUCCESS] Analysis saved for user {user_id} with document ID: {doc_ref.id}")
    return f"Successfully saved analysis for user {user_id} to Firestore."

def get_latest_analysis(user_id: str) -> dict:
    """Fetches the most recent analysis document for a user."""
    print(f"[INFO] Fetching latest portfolio analysis for user_id: {user_id}")
    query = (
        db.collection("portfolio_history")
        # .where("user_id", "==", user_id)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(1)
    )
    
    results = query.get()
    for doc in results:
        print(f"[SUCCESS] Found latest analysis for user {user_id} with document ID: {doc.id}")
        return doc.to_dict().get("analysis_data", {})
    
    print(f"[WARNING] No data found for user {user_id}.")
    return {"error": "No data found for this user."}