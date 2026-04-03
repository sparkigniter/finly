from app.backend.services.broker.interfaces.broker_service import BrokerService


class BrokerServiceProvider:
    """Provider for broker services."""

    def __init__(self, broker_service: BrokerService):
        self.service = broker_service

    def get_holdings(self, user_id: str):
        """Fetch the user's holdings from the broker."""
        return self.service.get_holdings(user_id)
