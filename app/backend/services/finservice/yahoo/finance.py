"""Module providing finance functionality."""
import yfinance as yf
from yfinance import Ticker


class YahooFinance:

    """YahooFinance class implementation."""
    def __init__(self, ticker: str):
        """Initializes a new instance of the class."""
        self.ticker: Ticker =  yf.Ticker(ticker)
        print("yfinance info {self.ticker_info}")

    def get_sector(self):
        """Retrieves the sector."""
        return self.ticker.info.get("sector")

    def get_pe_ratio(self):
        """Retrieves the pe ratio."""
        return self.ticker.info.get("trailingPE")

    def get_market_cap(self):
        """Retrieves the market cap."""
        return self.ticker.info.get("marketCap")

    def get_price(self):
        """Retrieves the price."""
        return self.ticker.info.get("currentPrice")

    def get_dividend_yield(self):
        """Retrieves the dividend yield."""
        return self.ticker.info.get("dividendYield")

    def get_enterprise_value(self):
        """Retrieves the enterprise value."""
        return self.ticker.info.get("enterpriseValue")  
    
    def get_enterprise_to_ebitda(self):
        """Retrieves the enterprise to ebitda."""
        return self.ticker.info.get("enterpriseToEbitda")

    def get_trailing_eps(self):
        """Retrieves the trailing eps."""
        return self.ticker.info.get("trailingEps")

    def get_trailing_pe(self):
        """Retrieves the trailing pe."""
        return self.ticker.info.get("trailingPE")

    def get_forward_pe(self):
        """Retrieves the forward pe."""
        return self.ticker.info.get("forwardPE")

    def industry(self):
        """Performs the industry operation."""
        return self.ticker.info.get("industry") 
    
    def get_beta(self):
        """Retrieves the beta."""
        return self.ticker.info.get("beta")

    def get_debt_to_equity(self):
        """Retrieves the debt to equity."""
        return self.ticker.info.get("debtToEquity")

    def dividend_rate(self):
        """Performs the dividend rate operation."""
        return self.ticker.info.get("dividendRate")

    def get_book_value(self):
        """Retrieves the book value."""
        return self.ticker.info.get("bookValue")

    def get_price_to_book(self):
        """Retrieves the price to book."""
        return self.ticker.info.get("priceToBook")

    def get_total_revenue(self):
        """Retrieves the total revenue."""
        return self.ticker.info.get("totalRevenue")

    def get_total_debt(self):
        """Retrieves the total debt."""
        return self.ticker.info.get("totalDebt")

    def get_total_cash(self):
        """Retrieves the total cash."""
        return self.ticker.info.get("totalCash")  


        
