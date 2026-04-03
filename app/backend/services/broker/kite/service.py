
import redis
from app.backend.services.broker.kite.client import KiteClient

class KiteBrokerService:
    """Service class responsible for handling business logic related to Kite Connect API interactions."""
    def __init__(self, client: KiteClient):
        self.client = client

    def get_holdings(self, user_id: str) -> list[dict]:
        """Fetches the user's holdings from the Kite Connect API."""
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True) #TODO: Create a Redis client provider in the container and use it here instead of creating a new instance 
        print(f"Getting holdings for user_id: {user_id}")
        print(self.client.get_client().api_key)   
        kite = self.client.get_client()
        key = "kite_access_token_" + user_id
        print(f"Fetching holdings for user_id: {user_id} with access token from Redis key: {key}")
        print(redis_client.get(key))
        kite.set_access_token(redis_client.get(key))
        try:
            holdings = kite.holdings()
            return holdings
        except Exception as e:
            raise Exception(f"Failed to fetch holdings: {str(e)}") from e