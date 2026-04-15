"""Module providing user functionality."""

from typing import Protocol


class User(Protocol):
    """User class implementation."""

    user_id: str
    email: str
    display_name: str

    def get_name(self) -> str:
        """Retrieves the name."""
        pass

    def get_email(self) -> str:
        """Retrieves the email."""
        pass

    def get_id(self) -> str:
        """Retrieves the id."""
        pass

    def set_token(self, token: str):
        """Sets the token."""
        pass

    def get_token(self) -> str:
        """Retrieves the token."""
        pass

    def set_refresh_token(self, refresh_token: str):
        """Sets the refresh token."""
        pass

    def get_refresh_token(self) -> str:
        """Retrieves the refresh token."""
        pass
