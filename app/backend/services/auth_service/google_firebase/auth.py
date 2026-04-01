"""Module responsible for handling authentication using Firebase."""

import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from firebase_admin import auth
from app.backend.services.auth_service.interfaces.user import User as UserInterface
from app.backend.services.auth_service.user import User
from app.backend.services.auth_service.token import Token


class Auth:
    def __init__(self):
        self.api_key = os.getenv("FIREBASE_API_KEY")
        self.auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"

    def register_user(
        self, email: str, password: str, username: str = None
    ) -> UserInterface:
        """Registers a new user with the provided email and password."""
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=username,
            disabled=False,
        )
        return User(user.uid, user.email, user.display_name)

    def authenticate(self, email: str, password: str) -> Token:
        """Authenticates a user with the provided credentials and returns a token."""
        try:
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True}
            # Added a 10-second timeout for safety
            response = requests.post(self.auth_url, json=payload, timeout=10)

            # Parse early so we can use it in the error blocks
            data = response.json()

            # Manually trigger the HTTPError if status is 4xx/5xx
            response.raise_for_status()

            # Success path
            token = Token(data["idToken"])
            return token

        except Timeout as exe:
            raise Exception(
                "Authentication request timed out. Please try again."
            ) from exe
        except ConnectionError as exe:
            raise Exception(
                "Network error: Could not reach the auth server.") from exe
        except HTTPError as exe:
            error_msg = (
                data.get("error", {}).get("message", "AUTH_FAILED")
                if data
                else "HTTP_ERROR"
            )
            raise Exception(error_msg) from exe
        except Exception as e:
            # Catch-all for unexpected issues
            raise Exception(f"An unexpected error occurred: {str(e)}") from e

    def verify_token(self, tokenString: str) -> Token:
        """Verifies the validity of a provided authentication token."""
        try:
            auth.verify_id_token(tokenString)
            return Token(tokenString=tokenString)
        except Exception as e:
            raise Exception(f"Token verification failed: {str(e)}") from e
