"""Schema definitions for protfolio."""
from pydantic import BaseModel, Field
from typing import List, Optional


class PortfolioInsights(BaseModel):
    """PortfolioInsights class implementation."""
    portfolio_health_score: float = Field(ge=0, le=100)
    risk_assessment: list[str] = []
    diversification_analysis: list[str] = []
    strategic_actions: list[str] = []


class PersonalizedInsight(BaseModel):
    """PersonalizedInsight class implementation."""
    user_profile: str
    portfolio_health_score: float = Field(ge=0, le=100)

    strengths: list[str] = []
    weaknesses: list[str] = []

    key_actions: list[str] = []
    warnings: list[str] = []

    time_horizon_advice: str


class PortfolioAnalysisResponse(BaseModel):
    """PortfolioAnalysisResponse class implementation."""
    portfolio_insights: PortfolioInsights
    personalized_insight: PersonalizedInsight
