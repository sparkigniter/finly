from app.backend.services.broker.kite.client import KiteClient
from app.backend.services.cache.provider import CacheProvider


class KiteBrokerService:
    """Service class responsible for handling business logic related to Kite Connect API interactions."""

    def __init__(self, client: KiteClient, cache: CacheProvider):
        self.client = client
        self.cache = cache

    def get_holdings(self) -> list[dict]:
        """Fetches the user's holdings from the Kite Connect API."""
        kite = self.client.get_client()
        kite.set_access_token(self.get_access_token())
        try:
            holdings = kite.holdings()
            return holdings
        except Exception as e:
            raise Exception(f"Failed to fetch holdings: {str(e)}") from e

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def get_access_token(self) -> str:
        return self.access_token
