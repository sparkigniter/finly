"""Module responsible for handling authentication using Firebase."""

import os
import requests
import firebase_admin
from requests.exceptions import HTTPError, ConnectionError, Timeout
from firebase_admin import auth
from app.backend.services.auth.interfaces.user import User as UserInterface
from app.backend.services.auth.user import User
from app.backend.services.auth.token import Token

class Auth:
    """Authentication class responsible for handling user registration, authentication, and token verification using Firebase."""

    def __init__(self):
        # API Key is used for the client-side 'signInWithPassword' REST fallback
        """Initializes a new instance of the class."""
        self.api_key = os.getenv("FIREBASE_API_KEY")
        self.auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        
        # Senior DevOps Note: Ensure the default app is initialized via FirebaseProvider 
        # before this class is instantiated, or verify_id_token will fail.

    def register_user(self, email: str, password: str, username: str = None) -> UserInterface:
        """Registers a new user with the provided email and password."""
        try:
            user = auth.create_user(
                email=email,
                email_verified=False,
                password=password,
                display_name=username,
                disabled=False,
            )
            return User(user.uid, user.email, user.display_name)
        except Exception as e:
            raise Exception(f"User registration failed: {str(e)}")

    def authenticate(self, email: str, password: str) -> Token:
        """Authenticates a user with the provided credentials and returns a token."""
        try:
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            # 10-second timeout to prevent hanging worker threads
            response = requests.post(self.auth_url, json=payload, timeout=10)
            data = response.json()
            response.raise_for_status()

            return Token(data["idToken"])

        except Timeout as exe:
            raise Exception("Authentication request timed out. Please try again.") from exe
        except ConnectionError as exe:
            raise Exception("Network error: Could not reach the Firebase auth server.") from exe
        except HTTPError as exe:
            error_msg = data.get("error", {}).get("message", "AUTH_FAILED")
            raise Exception(f"Authentication failed: {error_msg}") from exe
        except Exception as e:
            raise Exception(f"An unexpected error occurred during auth: {str(e)}") from e

    def verify_token(self, token_string: str) -> Token:
        """
        Verifies the validity of a provided authentication token.
        RCA for 'InvalidIdTokenError': This happens if 'aud' in JWT does not match 
        the projectId used in firebase_admin.initialize_app().
        """
        try:
            # check_revoked=True is a security best practice for production
            decoded_token = auth.verify_id_token(token_string, check_revoked=True)
            return Token(token_string=token_string)
        except auth.InvalidIdTokenError as e:
            # This is where your 'aud' mismatch is caught
            raise Exception(f"Invalid Token: Project ID mismatch or expired token. Details: {str(e)}")
        except Exception as e:
            raise Exception(f"Token verification failed: {str(e)}")
