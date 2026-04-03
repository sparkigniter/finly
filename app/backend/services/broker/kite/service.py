<<<<<<< HEAD

=======
import redis
>>>>>>> 7947a42c4410abee7c6cc6baa19f7e7ad1d999ca
from app.backend.services.broker.kite.client import KiteClient
from app.backend.services.cache.provider import CacheProvider


class KiteBrokerService:
    """Service class responsible for handling business logic related to Kite Connect API interactions."""
<<<<<<< HEAD
    def __init__(self, client: KiteClient, cache: CacheProvider):
=======

    def __init__(self, client: KiteClient):
>>>>>>> 7947a42c4410abee7c6cc6baa19f7e7ad1d999ca
        self.client = client
        self.cache = cache

    def get_holdings(self, user_id: str) -> list[dict]:
        """Fetches the user's holdings from the Kite Connect API."""
<<<<<<< HEAD
=======
        redis_client = redis.Redis(
            host="localhost", port=6379, decode_responses=True
        )  # TODO: Create a Redis client provider in the container and use it here instead of creating a new instance
>>>>>>> 7947a42c4410abee7c6cc6baa19f7e7ad1d999ca
        print(f"Getting holdings for user_id: {user_id}")
        print(self.client.get_client().api_key)
        kite = self.client.get_client()
        key = "kite_access_token_" + user_id
<<<<<<< HEAD
        print(f"Fetching holdings for user_id: {user_id} with access token from Redis key: {key}")
        kite.set_access_token(self.cache.get(key))
=======
        print(
            f"Fetching holdings for user_id: {user_id} with access token from Redis key: {key}"
        )
        print(redis_client.get(key))
        kite.set_access_token(redis_client.get(key))
>>>>>>> 7947a42c4410abee7c6cc6baa19f7e7ad1d999ca
        try:
            holdings = kite.holdings()
            return holdings
        except Exception as e:
            raise Exception(f"Failed to fetch holdings: {str(e)}") from e
