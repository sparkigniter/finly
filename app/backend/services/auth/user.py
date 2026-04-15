"""Module providing user functionality."""


class User:
    """User class implementation."""

    def __init__(self, user_id: str, email: str, display_name: str = None):
        """Initializes a new instance of the class."""
        self.user_id = user_id
        self.email = email
        self.display_name = display_name

    def to_dict(self):
        """Performs the to dict operation."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "display_name": self.display_name,
            "token": self.token,
            "refresh_token": self.refresh_token,
        }

    def get_name(self):
        """Retrieves the name."""
        return self.display_name

    def get_email(self):
        """Retrieves the email."""
        return self.email

    def get_id(self):
        """Retrieves the id."""
        return self.user_id

    def set_token(self, token: str):
        """Sets the token."""
        self.token = token

    def get_token(self) -> str:
        """Retrieves the token."""
        return self.token

    def set_refresh_token(self, refresh_token: str):
        """Sets the refresh token."""
        self.refresh_token = refresh_token

    def get_refresh_token(self) -> str:
        """Retrieves the refresh token."""
        return self.refresh_token
