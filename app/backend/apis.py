"""This module defines the API endpoints for the portfolio analysis application."""
from datetime import timezone, datetime
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.ai.google_vertex.agents.tools.firestore_datastore import get_latest_analysis
from app.backend.services.container import Container
from app.backend.dtos.create_user import UserCreateDto
from app.backend.dtos.login import LoginDto
from app.backend.services.auth_service.middlewares.auth_middleware import verify_token
from app.backend.services.auth_service.token import Token

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
    allow_origins=origins,  # Allow your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)


@app.post("/analyze-portfolio")
async def analyze_portfolio(
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=3600)
