"""Module providing auth_service functionality."""
from typing import Protocol
from app.backend.services.auth.interfaces.user import User as UserInterface


class AuthService(Protocol):
    """AuthService class implementation."""
    def register_user(
        self, email: str, password: str, username: str = None
    ) -> UserInterface:
        """Performs the register user operation."""
        pass

    # def authenticate(self, username: str, password: str) -> bool:
    #     pass

    # def verify_token(self, token: str) -> bool:
    #     pass

    # def get_user_id(self, token: str) -> str:
    #     pass

