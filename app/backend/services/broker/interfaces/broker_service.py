from typing import Protocol
from app.backend.services.broker.interfaces.holdings import Holdings
<<<<<<< HEAD
=======

>>>>>>> 7947a42c4410abee7c6cc6baa19f7e7ad1d999ca

class BrokerService(Protocol):
    """Protocol for broker services to implement."""

    def get_holdings(self, access_token: str) -> list[Holdings]:
        """Fetch the user's holdings from the broker."""
        pass
