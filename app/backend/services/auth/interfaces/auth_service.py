from typing import Protocol
from app.backend.services.auth.interfaces.user import User as UserInterface


class AuthService(Protocol):
    def register_user(self, email: str, password: str, username: str = None) -> UserInterface:
        pass

    # def authenticate(self, username: str, password: str) -> bool:
    #     pass

    # def verify_token(self, token: str) -> bool:
    #     pass

    # def get_user_id(self, token: str) -> str:
    #     pass
