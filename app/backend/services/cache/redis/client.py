"""Redis client wrapper for managing Redis connections and operations."""

import os

import redis


class RedisClient:
    """A simple Redis client wrapper to manage Redis connections and operations."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """Initializes a new instance of the class."""
        self.client = redis.Redis(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            db=int(os.environ["REDIS_DB"]),
            decode_responses=True,
        )

    def set(self, key: str, value: str, ex: int = None) -> bool:
        """Set a value in Redis with an optional expiration time."""
        return self.client.set(name=key, value=value, ex=ex)

    def get(self, key: str) -> str:
        """Get a value from Redis by key."""
        return self.client.get(name=key)

    def delete(self, key: str) -> int:
        """Delete a key from Redis."""
        return self.client.delete(key)

    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        return self.client.exists(key) == 1

    def flushdb(self) -> bool:
        """Flush the current database in Redis."""
        return self.client.flushdb()

