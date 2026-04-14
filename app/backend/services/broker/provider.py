from app.backend.services.broker.interfaces.broker_service import BrokerService

class BrokerServiceProvider:
    """Provider for broker services."""

    def __init__(self, broker_service: BrokerService):
        self.service = broker_service

    def get_holdings(self):
        """Fetch the user's holdings from the broker."""
        return self.service.get_holdings()
    
    def set_access_token(self, access_token: str):
        self.service.set_access_token(access_token)
    
    def get_access_token(self) -> str:
        return self.service.get_access_token()
        
