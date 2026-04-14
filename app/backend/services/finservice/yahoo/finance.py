import yfinance as yf
from yfinance import Ticker

class YahooFinance:

    def __init__(self, ticker: str):
        self.ticker: Ticker =  yf.Ticker(ticker)
        print("yfinance info {self.ticker_info}")
        

    def get_sector(self):
        return self.ticker.info.get("sector")
    
    def get_pe_ratio(self):
        return self.ticker.info.get("trailingPE")
    
    def get_market_cap(self):
        return self.ticker.info.get("marketCap")

    def get_price(self):
        return self.ticker.info.get("currentPrice")
    
    def get_dividend_yield(self):
        return self.ticker.info.get("dividendYield")
    
    def get_enterprise_value(self):
        return self.ticker.info.get("enterpriseValue")  
    
    def get_enterprise_to_ebitda(self):
        return self.ticker.info.get("enterpriseToEbitda")
    
    def get_trailing_eps(self):
        return self.ticker.info.get("trailingEps")
    
    def get_trailing_pe(self):
        return self.ticker.info.get("trailingPE")
    
    def get_forward_pe(self):
        return self.ticker.info.get("forwardPE")
    
    def industry(self):
        return self.ticker.info.get("industry") 
    
    def get_beta(self):
        return self.ticker.info.get("beta")

    def get_debt_to_equity(self):
        return self.ticker.info.get("debtToEquity")
    
    def dividend_rate(self):
        return self.ticker.info.get("dividendRate")

    def get_book_value(self):
        return self.ticker.info.get("bookValue")
    
    def get_price_to_book(self):
        return self.ticker.info.get("priceToBook")
    
    def get_total_revenue(self):
        return self.ticker.info.get("totalRevenue")

    def get_total_debt(self):
        return self.ticker.info.get("totalDebt")
    
    def get_total_cash(self):
        return self.ticker.info.get("totalCash")  


        