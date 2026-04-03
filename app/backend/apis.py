"""This module defines the API endpoints for the portfolio analysis application."""

from datetime import timezone, datetime
import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
from dotenv import load_dotenv
from app.ai.google_vertex.agents.tools.firestore_datastore import get_latest_analysis
from app.backend.services.container import Container
from app.backend.dtos.create_user import UserCreateDto
from app.backend.dtos.login import LoginDto
from app.backend.services.auth.middlewares.auth_middleware import verify_token
from app.backend.services.auth.token import Token
from app.backend.services.broker.interfaces.holdings import Holdings

# TODO: Create a Redis client provider in the container and use it here
# instead of creating a new instance
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

load_dotenv()

app = FastAPI()

# 1. Define the origins that are allowed to talk to your server
# Define the origins that are allowed to hit your API
origins = [
    "https://localhost",  # Standard Capacitor Android/iOS origin
    "http://localhost",  # Some local dev environments
    "http://localhost:5173",  # Your Vite dev server
    "https://api.manadakathe.com",  # Your production frontend domain
]

# 2. Add the middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)


@app.post("/analyze-portfolio-file")
async def analyze_portfolio_file(
    file: UploadFile = File(...), token: Token = Depends(verify_token)
):
    """API to analyze the portfolio data"""

    user_id = token.get_claim("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    portfolio_data: dict = await Container.get().get_file_service.parse_file(file)

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
    holdings = broker_service.get_holdings(user_id)
    queue_data: dict = {
        "data": holdings,
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
    data = get_latest_analysis(user_id)
    return data


@app.post("/user")
async def register_user(user: UserCreateDto):
    """API to register a new user."""
    user = Container.get().get_auth_service_provider.register_user(
        user.email, user.password
    )
    return "success"


@app.post("/login")
async def authenticate_user(user: LoginDto):
    """API to authenticate a user and return a token."""
    try:
        token = Container.get().get_auth_service_provider.authenticate(
            user.email, user.password
        )
        return token.to_dict()
    except Exception as e:
        return str(e)


@app.get("/broker/kite/login")
async def kite_login(token: Token = Depends(verify_token)):
    """API to handle Kite Connect login."""
    kite = Container.get().get_kite_client.get_client()
    login_url = kite.login_url()
    login_url += f"&redirect_params=user_id%3D{token.get_claim('user_id')}"
    return {"login_url": login_url}


@app.get("/broker/kite/callback")
async def kite_callback(request_token: str, user_id: str):
    """API to handle Kite Connect callback."""
    kite = Container.get().get_kite_client.get_client()
    data = kite.generate_session(request_token,
                                 api_secret=os.getenv("KITE_API_SECRET"))
    kite.set_access_token(data["access_token"])
    key = "kite_access_token_" + user_id
    redis_client.set(key, data["access_token"])
    return {"message": "Kite Connect login successful"}


@app.get("/broker/kite/holdings")
async def get_holdings(
        token: Token = Depends(verify_token),
        request_token: str = None):
    """API to fetch Kite Connect holdings."""
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=3600)
