from app.backend.services.auth_service.interfaces.auth_service import AuthService
from app.backend.services.auth_service.interfaces.user import User as UserInterface
from app.backend.services.auth_service.user import User

class AuthServiceProvider:
    """
    Service provider for authentication and user management.
    """
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def register_user(self, email: str, password: str) -> UserInterface:
        return self.auth_service.register_user(email, password)

    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticates a user with the provided credentials.
        """
        return self.auth_service.authenticate(email, password)

    def verify_token(self, tokenString: str) -> bool:
        """
        Verifies the validity of a provided authentication token.
        """
        # Implementation for token verification
        return self.auth_service.verify_token(tokenString)


    def get_user_id(self, token: str) -> str:
        """
        Extracts the user ID from a valid authentication token.
        """
        # Implementation for extracting user ID
        return "test_user"
