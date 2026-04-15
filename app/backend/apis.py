"""This module defines the API endpoints for the portfolio analysis application."""

from datetime import timezone, datetime
import json
import os
import uuid
import logging
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from app.ai.google_vertex.agents.tools.firestore_datastore import (
    get_latest_analysis,
    store_portfolio_analysis,
)
from app.backend.services.container import Container
from app.backend.dtos.create_user import UserCreateDto
from app.backend.dtos.login import LoginDto
from app.backend.services.auth.middlewares.auth import verify_token
from app.backend.services.auth.token import Token
from app.backend.services.broker.interfaces.holdings import Holdings
from app.backend.services.protfolio.service import PortfolioService

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Define CORS origins from environment variable or use defaults
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
origins = [origin.strip() for origin in cors_origins if origin.strip()]

# Add the middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-portfolio-file")
async def analyze_portfolio_file(
    file: UploadFile = File(...), token: Token = Depends(verify_token)
):
    """API to analyze the portfolio data from a CSV file."""
    
    user_id = token.get_claim("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Validate file size and type
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
    
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=415, detail="Invalid file type. Only CSV files are accepted.")

    try:
        portfolio_data: dict = await Container.get().get_file_service.parse_file(file)
    except Exception as e:
        logger.error(f"File parsing failed for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail="Failed to parse file. Please ensure it is a valid CSV.")

    queue_data: dict = {
        "data": portfolio_data,
        "pushed_at": datetime.now(
            timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "user_id": user_id,
        "status": "pending",
    }
    Container.get().get_portfolio_analysis_queue.push(queue_data)
    return {
        "status": "success",
        "message": "We are analysing the stocks. You will get email notification once succeeded.",
    }

@app.post("/analyze-portfolio")
async def analyze_portfolio_(token: Token = Depends(verify_token)):
    """Helper function to analyze portfolio data."""
    broker_service = Container.get().get_broker_service_provider
    user_id = token.get_claim("user_id")
    
    try:
        holdings = broker_service.get_holdings(user_id)
    except Exception as e:
        logger.error(f"Failed to retrieve holdings for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve holdings from broker.")
    
    holdings_data = [
        {
            "symbol": h["tradingsymbol"],
            "quantity": h["quantity"],
            "average_price": h["average_price"],
            "last_price": h["last_price"],
            "pnl": h["pnl"],
            "exchange": h["exchange"],
        }
        for h in holdings
    ]
    logger.info(f"Retrieved holdings for user {user_id}: {len(holdings_data)} stocks")
    
    queue_data: dict = {
        "data": holdings_data,
        "pushed_at": datetime.now(
            timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "user_id": user_id,
        "status": "pending",
    }
    Container.get().get_portfolio_analysis_queue.push(queue_data)
    return {
        "status": "success",
        "message": "We are analysing the stocks. You will get email notification once succeeded.",
    }

@app.get("/portfolio")
async def fetch_ui_data(token: Token = Depends(verify_token)):
    """API to fetch the latest portfolio analysis data for the UI."""
    user_id = token.get_claim("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        data = get_latest_analysis(user_id)
    except Exception as e:
        logger.error(f"Failed to fetch portfolio analysis for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio data.")
    
    return data

@app.post("/user")
async def register_user(user: UserCreateDto):
    """API to register a new user."""
    try:
        Container.get().get_auth_service_provider.register_user(
            user.email, user.password
        )
        return {"status": "success", "message": "User registered successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"User registration failed for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed. Please try again.")

@app.post("/login")
async def authenticate_user(user: LoginDto):
    """API to authenticate a user and return a token."""
    try:
        token = Container.get().get_auth_service_provider.authenticate(
            user.email, user.password
        )
        return token.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    except Exception as e:
        logger.error(f"Authentication failed for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Authentication failed. Please try again.")

@app.get("/broker/kite/login")
async def kite_login(token: Token = Depends(verify_token)):
    """API to handle Kite Connect login."""
    try:
        kite = Container.get().get_kite_client.get_client()
        login_url = kite.login_url()
        login_url += f"&redirect_params=user_id%3D{token.get_claim('user_id')}"
        return {"login_url": login_url}
    except Exception as e:
        logger.error(f"Kite login URL generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate login URL.")

@app.get("/broker/kite/callback")
async def kite_callback(request_token: str, user_id: str, client_type: str = Query("web")):
    """
    API to handle Kite Connect callback.
    
    Args:
        request_token: OAuth request token from Kite
        user_id: User ID for session management
        client_type: Either 'mobile' or 'web' to determine response format
    
    Returns:
        RedirectResponse for mobile clients, JSON response for web clients
    """
    try:
        kite = Container.get().get_kite_client.get_client()
        data = kite.generate_session(request_token,
                                     api_secret=os.getenv("KITE_API_SECRET"))
        kite.set_access_token(data["access_token"])
        broker_service = Container.get().get_broker_service_provider
        broker_service.set_access_token(data["access_token"])
        holdings = broker_service.get_holdings()
        logger.info(f"Retrieved {len(holdings)} holdings for user {user_id}")
        
        portfolio_service = PortfolioService(holdings, True)
        portfolio_data = {
            "portfolio": {
                "summary": portfolio_service.get_summary(),
                "top_holdings": portfolio_service.get_top_holdings(),
                "diversification_score": portfolio_service.get_diversification_score(),
                "worst_performing_stocks": portfolio_service.get_worst_performer(),
                "best_performing_stocks": portfolio_service.get_best_performer(),
                "stocks": portfolio_service.get_stock_breakdown(),
            }
        }
        store_portfolio_analysis(portfolio_data, user_id)
        
        request_id = uuid.uuid4().hex
        portfolio_analysis_queue_data = {
            "user_id": user_id,
            "request_id": request_id,
            "pushed_at": datetime.now(
                timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "portfolio": {
                "summary": portfolio_service.get_summary(),
                "top_holdings": portfolio_service.get_top_holdings(),
                "diversification_score": portfolio_service.get_diversification_score(),
                "worst_performing_stocks": portfolio_service.get_worst_performer(),
                "best_performing_stocks": portfolio_service.get_best_performer(),
                "sector_allocation": portfolio_service.get_sector_allocation(),
            },
        }
        Container.get().get_portfolio_analysis_queue.push(
            json.dumps(portfolio_analysis_queue_data)
        )
        
        # Return appropriate response based on client type
        if client_type.lower() == "mobile":
            return RedirectResponse(
                url=f"finly://broker-sync?request_token={request_token}&status=success"
            )
        else:
            return {
                "status": "success",
                "message": "Kite Connect login successful and portfolio analysis started.",
                "request_id": request_id,
            }
    
    except Exception as e:
        logger.error(f"Kite callback failed for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process Kite callback.")

@app.get("/broker/kite/holdings")
async def get_holdings(
        token: Token = Depends(verify_token),
        request_token: str = None):
    """API to fetch Kite Connect holdings."""
    try:
        data = Container.get().get_broker_service_provider.get_holdings(
            token.get_claim("user_id")
        )
        return [
            Holdings(
                symbol=h["tradingsymbol"],
                quantity=h["quantity"],
                average_price=h["average_price"],
                last_price=h["last_price"],
                pnl=h["pnl"],
                exchange=h["exchange"],
            )
            for h in data
        ]
    except Exception as e:
        logger.error(f"Failed to fetch holdings: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve holdings.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=3600)
