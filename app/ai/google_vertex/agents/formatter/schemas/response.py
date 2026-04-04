from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

# --- SCHEMA DEFINITIONS ---

class Recommendation(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_BUY = "STRONG_BUY"

class IndividualStock(BaseModel):
    ticker: str = Field(..., description="Ticker symbol (e.g., RELIANCE.NS)")
    sector: str = Field(..., description="Industry sector (e.g., Energy, IT)")
    quantity: int
    buy_price: float
    current_price: float
    performance_pct: float = Field(..., description="Unrealized PnL %")
    total_gain_loss: float = Field(..., description="Absolute PnL in currency")
    recommendation: Recommendation
    
    # Advanced Insights
    technical_view: str = Field(..., description="Summary of RSI, MACD, and Moving Averages")
    rsi_value: Optional[float] = Field(None, description="Relative Strength Index (0-100)")
    fundamental_summary: str = Field(..., description="Summary of P/E, Debt/Equity, and EPS")
    pe_ratio: Optional[float] = Field(None, description="Price to Earnings Ratio")
    
    latest_news: str = Field(..., description="Latest market-moving headline")
    dividend_yield: float = Field(default=0.0, description="Annual dividend yield %")
    market_cap: str = Field(..., description="Market Cap (e.g., Large Cap, Mid Cap)")

class PortfolioSummary(BaseModel):
    total_investment: float
    current_value: float
    total_returns: float
    overall_performance_pct: float
    diversification_score: float = Field(..., ge=0, le=100)
    risk_profile: str = Field(..., description="Conservative, Balanced, or Aggressive")
    top_sector: str = Field(..., description="Sector with highest allocation")

class PortfolioBreakdown(BaseModel):
    individual_stocks: List[IndividualStock]
    portfolio_summary: PortfolioSummary