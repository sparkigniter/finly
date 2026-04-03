from typing import Protocol

class Cache(Protocol):
    """Protocol for cache services to implement."""
    def set(self, key: str, value: str, expire: int = None) -> None:
        """Set a value in the cache with an optional expiration time."""
        pass

    def get(self, key: str) -> str:
        """Get a value from the cache by key."""
        pass

    def delete(self, key: str) -> None:
        """Delete a value from the cache by key."""

    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        pass
    
    def flushdb(self) -> None:
        """Flush the current database in the cache."""
        pass
        