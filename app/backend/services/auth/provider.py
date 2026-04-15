"""Module responsible for providing authentication services and user management."""

from app.backend.services.auth.interfaces.auth_service import AuthService
from app.backend.services.auth.interfaces.user import User as UserInterface


class AuthServiceProvider:
    """
    Service provider for authentication and user management.
    """

    def __init__(self, auth_service: AuthService):
        """Initializes a new instance of the class."""
        self.auth_service = auth_service

    def register_user(self, email: str, password: str) -> UserInterface:
        """Registers a new user with the provided email and password."""
        return self.auth_service.register_user(email, password)

    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticates a user with the provided credentials.
        """
        return self.auth_service.authenticate(email, password)

    def verify_token(self, token_string: str) -> bool:
        """
        Verifies the validity of a provided authentication token.
        """
        # Implementation for token verification
        return self.auth_service.verify_token(token_string)

    def get_user_id(self, token: str) -> str:
        """
        Extracts the user ID from a valid authentication token.
        """
        # Implementation for extracting user ID
        return self.auth_service.get_user_id(token)
