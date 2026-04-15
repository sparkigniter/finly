"""Schema definitions for stock."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Recommendation(str, Enum):
    """Recommendation class implementation."""

    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_BUY = "STRONG_BUY"


class MarketCap(str, Enum):
    """MarketCap class implementation."""

    LARGE = "Large Cap"
    MID = "Mid Cap"
    SMALL = "Small Cap"


class StockInsight(BaseModel):
    """StockInsight class implementation."""

    reason: str
    risks: list[str] = []
    opportunities: list[str] = []
    action: str


class Stock(BaseModel):
    """Stock class implementation."""

    tradingsymbol: str
    recommendation: Recommendation

    technical_view: Optional[str] = None
    fundamental_summary: Optional[str] = None

    rsi_value: Optional[float] = Field(default=None, ge=0, le=100)
    pe_ratio: Optional[float] = None

    latest_news: Optional[str] = None
    market_cap: MarketCap

    insight: StockInsight


class StockAnalysisResponse(BaseModel):
    """StockAnalysisResponse class implementation."""

    stocks: list[Stock]
