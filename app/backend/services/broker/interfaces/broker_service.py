from typing import Protocol
from app.backend.services.broker.interfaces.holdings import Holdings


class BrokerService(Protocol):
    """Protocol for broker services to implement."""

    def get_holdings(self, access_token: str) -> list[Holdings]:
        """Fetch the user's holdings from the broker."""
        pass
