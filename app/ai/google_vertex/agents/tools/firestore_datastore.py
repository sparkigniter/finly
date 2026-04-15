"""Implements Firestore integration for storing and retrieving portfolio analysis results."""

import os
from google.cloud import firestore

# Initialize the Firestore client
db = firestore.Client(database="finly", project=os.environ.get("PROJECT_ID"))
APP_ID = os.environ.get("APP_ID", "finly-app")


@firestore.transactional
def update_portfolio_transaction(transaction, user_id, analysis_data):
    """
    RCA: Prevents partial updates or race conditions where
    multiple analysis runs might trigger for the same user.
    """
    collection_ref = db.collection("portfolio_history")
    query = collection_ref.where("user_id", "==", user_id)

    existing_docs = query.get(transaction=transaction)

    # Clean up old records to maintain a 'latest' state if preferred,
    # or skip this step to keep full historical logs.
    for doc in existing_docs:
        transaction.delete(doc.reference)

    new_doc_ref = collection_ref.document()
    data = {
        "user_id": user_id,
        "analysis_data": analysis_data,
        "created_at": firestore.SERVER_TIMESTAMP,
        "version": 1,
    }
    transaction.set(new_doc_ref, data)
    return new_doc_ref.id


@firestore.transactional
def patch_portfolio_transaction(transaction, doc_ref, stock_insights: list[dict] | None, protfolio_insights: dict | None):
    """Updates the transaction in Firestore with analyzed insights."""
    snapshot = doc_ref.get(transaction=transaction)
    if not snapshot.exists:
        raise Exception("Document not found")

    current_data = snapshot.to_dict()
    analysis_data = current_data.get("analysis_data", {})
    portfolio = analysis_data.get("portfolio", {})
    print(f"store data for {protfolio_insights}")
    if protfolio_insights is not None:
        transaction.update(doc_ref,
                           {"analysis_data.portfolio.protfolio_insights": protfolio_insights,
                            "updated_at": firestore.SERVER_TIMESTAMP,
                            },
                           )  # add portfolio-level insights
    if stock_insights is not None:
        existing_stocks = portfolio.get("stocks", [])
        symbol_to_idx = {
            s.get("tradingsymbol"): i for i, s in enumerate(existing_stocks)
        }
        for stock in stock_insights:
            symbol = stock.get("tradingsymbol")
            if symbol in symbol_to_idx:
                idx = symbol_to_idx[symbol]
                existing_stocks[idx]["insight"] = stock.get("insight")
                existing_stocks[idx]["market_cap"] = stock.get("market_cap")
                existing_stocks[idx]["rsi_value"] = stock.get("rsi_value")
                existing_stocks[idx]["pe_ratio"] = stock.get("pe_ratio")
                existing_stocks[idx]["latest_news"] = stock.get("latest_news")
                existing_stocks[idx]["technical_view"] = stock.get(
                    "technical_view")
                existing_stocks[idx]["fundamental_summary"] = stock.get(
                    "fundamental_summary"
                )
                existing_stocks[idx]["recommendation"] = stock.get(
                    "recommendation")
            else:
                # INSERT CASE: Append the new stock dictionary if it doesn't
                # exist
                existing_stocks.append(stock)

        transaction.update(
            doc_ref,
            {
                "analysis_data.portfolio.stocks": existing_stocks,
                "updated_at": firestore.SERVER_TIMESTAMP,
            },
        )

    return True


def store_portfolio_analysis(analysis_data: dict, user_id: str) -> str:
    """Entry point to create a new analysis record."""
    transaction = db.transaction()
    try:
        new_id = update_portfolio_transaction(
            transaction, user_id, analysis_data)
        print(f"[SUCCESS] Portfolio stored ID: {new_id}")
        return new_id
    except Exception as e:
        print(f"[ERROR] Transaction failed: {str(e)}")
        raise e


def patch_portfolio_analysis(
    user_id: str,
    stock_insights: list[dict] | None,
    protfolio_insights: list[dict] | None,
):
    """
    Finds the latest analysis for a user and appends new stocks to it.
    """
    collection_ref = db.collection("portfolio_history")

    # 1. Find the latest document reference
    docs = (
        collection_ref.where("user_id", "==", user_id)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(1)
        .get()
    )

    if not docs:
        print(f"[WARNING] No existing analysis found for {user_id} to patch.")
        return None

    target_doc_ref = docs[0].reference
    transaction = db.transaction()

    try:
        patch_portfolio_transaction(
            transaction, target_doc_ref, stock_insights, protfolio_insights
        )
        print(f"[SUCCESS] Patch successful {stock_insights}")
        print(f"[SUCCESS] Stocks appended to document: {target_doc_ref.id}")
    except Exception as e:
        print(f"[ERROR] Patch failed: {str(e)}")
        raise e


def get_latest_analysis(user_id: str) -> dict:
    """Fetches the most recent analysis document for a user."""
    collection_ref = db.collection("portfolio_history")
    query = (
        collection_ref.where("user_id", "==", user_id)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(1)
    )

    results = query.get()
    for doc in results:
        return doc.to_dict().get("analysis_data", {})

    return {"error": "No data found for this user."}


def get_stocks(user_id: str) -> dict:
    """Fetches the most recent analysis document for a user."""
    collection_ref = db.collection("portfolio_history")
    query = collection_ref.where("user_id", "==", user_id)
    results = query.get()
    for doc in results:
        return (
            doc.to_dict()
            .get("analysis_data", {})
            .get("portfolio", {})
            .get("stocks", [])
        )
    return []

def get_sector(symbol: str) -> str: 
    """Retrieves the sector."""
    collection_ref = db.collection("stock_details")
    query = collection_ref.where("tradingsymbol", "==", symbol)
    results = query.get()
    for doc in results:
        return doc.to_dict().get("sector")
    return False


def add_to_stock_details(tradingsymbol: str, data: dict):
    """Saves stock details into the standard datastore."""
    collection_ref = db.collection("stock_details")
    query = collection_ref.where("tradingsymbol", "==", tradingsymbol)
    results = query.get()
    if not results:
        return False
    results.append(data)
    return True


