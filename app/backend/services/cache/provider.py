"""Module providing provider functionality."""
from app.backend.services.cache.interfaces.cache import Cache


class CacheProvider:
    """Provider for cache services."""

    def __init__(self, client: Cache):
        """Initializes a new instance of the class."""
        self.client = client

    def set(self, key: str, value: str, expire: int = None):
        """Set a value in the cache with an optional expiration time."""
        self.client.set(key, value, expire)

    def get(self, key: str) -> str:
        """Get a value from the cache."""
        return self.client.get(key)

    def delete(self, key: str):
        """Delete a value from the cache."""
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        return self.client.exists(key)

    def flushdb(self):
        """Flush the current database in the cache."""
        self.client.flushdb()

