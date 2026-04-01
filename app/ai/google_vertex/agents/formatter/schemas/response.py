"""Defines the response schema for the Formatter Agent."""
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class Recommendation(str, Enum):
    """Enumeration for stock recommendations."""
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class IndividualStock(BaseModel):
    """Schema representing the structured analysis of an individual stock."""
    ticker: str = Field(...,
                        description="The stock ticker symbol (e.g., RELIANCE)")
    performance_pct: float = Field(...,
                                   description="Percentage change in performance")
    total_gain_loss: float = Field(...,
                                   description="Absolute profit or loss amount")
    recommendation: Recommendation
    technical_view: str = Field(
        ..., description="Short-term technical analysis summary"
    )
    fundamental_summary: str = Field(
        ..., description="Key fundamental health indicators"
    )
    latest_news: str = Field(...,
                             description="Most recent relevant news headline")
    dividend_yield: float = Field(default=0.0)
    sector: str
    market_cap: str


class PortfolioSummary(BaseModel):
    """Schema representing the overall portfolio analysis summary."""
    total_investment: float
    total_returns: float
    overall_performance_pct: float
    diversification_score: float = Field(
        ..., ge=0, le=100, description="Score from 0-100"
    )


class PortfolioBreakdown(BaseModel):
    """The root schema for the Financial Advisory Agent response."""

    individual_stocks: List[IndividualStock]
    portfolio_summary: PortfolioSummary
