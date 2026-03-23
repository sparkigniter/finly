from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Recommendation(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"

class IndividualStock(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol (e.g., RELIANCE)")
    performance_pct: float = Field(..., description="Percentage change in performance")
    total_gain_loss: float = Field(..., description="Absolute profit or loss amount")
    recommendation: Recommendation
    technical_view: str = Field(..., description="Short-term technical analysis summary")
    fundamental_summary: str = Field(..., description="Key fundamental health indicators")
    latest_news: str = Field(..., description="Most recent relevant news headline")
    dividend_yield: float = Field(default=0.0)
    sector: str
    market_cap: str

class PortfolioSummary(BaseModel):
    total_investment: float
    total_returns: float
    overall_performance_pct: float
    diversification_score: float = Field(..., ge=0, le=100, description="Score from 0-100")

class PortfolioBreakdown(BaseModel):
    """The root schema for the Financial Advisory Agent response."""
    individual_stocks: List[IndividualStock]
    portfolio_summary: PortfolioSummary
