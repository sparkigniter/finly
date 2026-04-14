from typing import List, Dict, Any
from enum import Enum
import logging

from app.backend.services.finservice.yahoo.finance import YahooFinance

logger = logging.getLogger(__name__)


# ============================================================================
# CONSTANTS & ENUMS
# ============================================================================

class RiskLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

UNKNOWN_SECTOR = "Unknown"
DEFAULT_TOP_N = 5


# ============================================================================
# EXCEPTIONS
# ============================================================================

class PortfolioError(Exception):
    pass

class InvalidHoldingError(PortfolioError):
    pass

class EmptyPortfolioError(PortfolioError):
    pass


# ============================================================================
# SERVICE
# ============================================================================

class PortfolioService:

    def __init__(self, holdings: List[Dict[str, Any]], enrich: bool = True):
        if not holdings:
            raise EmptyPortfolioError("Portfolio data cannot be empty.")

        self._validate_holdings(holdings)
        self.holdings = holdings

        if enrich:
            self._enrich_holdings()

    # ========================================================================
    # VALIDATION
    # ========================================================================

    def _validate_holdings(self, holdings):
        required = {"tradingsymbol", "quantity", "average_price", "last_price"}

        for i, h in enumerate(holdings):
            missing = required - h.keys()
            if missing:
                raise InvalidHoldingError(f"Holding {i} missing keys: {missing}")

            for field in ["quantity", "average_price", "last_price"]:
                if not isinstance(h[field], (int, float)) or h[field] < 0:
                    raise InvalidHoldingError(f"{field} must be non-negative")

    # ========================================================================
    # CORE CALCULATIONS
    # ========================================================================

    def _pnl(self, h):
        return (h["last_price"] - h["average_price"]) * h["quantity"]

    def _value(self, h):
        return h["last_price"] * h["quantity"]

    def _cost(self, h):
        return h["average_price"] * h["quantity"]

    def _roi(self, h):
        cost = self._cost(h)
        return round((self._pnl(h) / cost) * 100, 2) if cost > 0 else 0.0

    # ========================================================================
    # ENRICHMENT (OPTIMIZED)
    # ========================================================================

    def _enrich_holdings(self):
        for h in self.holdings:
            try:
                yahoo = YahooFinance(self._to_yahoo_symbol(h))

                h.update({
                    "sector": h.get("sector") or yahoo.get_sector(),
                    "industry": yahoo.industry(),
                    "pe_ratio": yahoo.get_pe_ratio(),
                    "market_cap": yahoo.get_market_cap(),
                    "dividend_yield": yahoo.get_dividend_yield(),
                    "debt_to_equity": yahoo.get_debt_to_equity(),
                    "beta": yahoo.get_beta(),
                })

            except Exception as e:
                logger.warning(f"Failed to enrich {h['tradingsymbol']}: {e}")

    def _to_yahoo_symbol(self, h):
        suffix = "BO" if h.get("exchange") == "BSE" else "NS"
        return f"{h['tradingsymbol']}.{suffix}"

    # ========================================================================
    # PUBLIC METHODS
    # ========================================================================

    def get_summary(self):
        total_inv = sum(self._cost(h) for h in self.holdings)
        total_val = sum(self._value(h) for h in self.holdings)
        total_pnl = total_val - total_inv

        gainers = [h for h in self.holdings if self._pnl(h) > 0]

        return {
            "total_investment": round(total_inv, 2),
            "total_current_value": round(total_val, 2),
            "total_pnl": round(total_pnl, 2),
            "overall_roi_pct": round((total_pnl / total_inv * 100), 2) if total_inv > 0 else 0,
            "holdings_count": len(self.holdings),
            "gainers_count": len(gainers),
            "win_rate": round(len(gainers) / len(self.holdings) * 100, 2),
        }

    def get_top_holdings(self, n=DEFAULT_TOP_N):
        sorted_h = sorted(self.holdings, key=self._value, reverse=True)[:n]

        return [
            {
                "tradingsymbol": h["tradingsymbol"],
                "roi": self._roi(h),
                "value": round(self._value(h), 2)
            }
            for h in sorted_h
        ]

    def get_stock_breakdown(self):
        return [
            {
                "tradingsymbol": h["tradingsymbol"],
                "current_value": round(self._value(h), 2),
                "pnl": round(self._pnl(h), 2),
                "roi": self._roi(h),
                "sector": h.get("sector", UNKNOWN_SECTOR),
                "pe_ratio": h.get("pe_ratio"),
                "market_cap": h.get("market_cap"),
            }
            for h in self.holdings
        ]

    def get_diversification_score(self):
        total = sum(self._value(h) for h in self.holdings)
        if total <= 0:
            return 0.0

        hhi = sum((self._value(h) / total) ** 2 for h in self.holdings)
        n = len(self.holdings)

        if n <= 1:
            return 0.0

        return round(((1 - hhi) / (1 - (1 / n))) * 100, 2)

    def get_sector_allocation(self):
        total = sum(self._value(h) for h in self.holdings)
        allocation = {}

        for h in self.holdings:
            sector = h.get("sector", UNKNOWN_SECTOR)
            val = self._value(h)

            allocation.setdefault(sector, {"value": 0})
            allocation[sector]["value"] += val

        for sec in allocation:
            val = allocation[sec]["value"]
            allocation[sec] = {
                "value": round(val, 2),
                "percentage": round(val / total * 100, 2) if total > 0 else 0
            }

        return allocation
    
    def get_best_performer(self):
        if not self.holdings:
            return None

        best = max(self.holdings, key=self._roi)

        return {
            "tradingsymbol": best["tradingsymbol"],
            "roi": self._roi(best),
            "pnl": round(self._pnl(best), 2),
            "current_value": round(self._value(best), 2),
        }


    def get_worst_performer(self):
        if not self.holdings:
            return None

        worst = min(self.holdings, key=self._roi)

        return {
            "tradingsymbol": worst["tradingsymbol"],
            "roi": self._roi(worst),
            "pnl": round(self._pnl(worst), 2),
            "current_value": round(self._value(worst), 2),
        }