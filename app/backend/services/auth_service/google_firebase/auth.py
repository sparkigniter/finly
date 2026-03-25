import firebase_admin
import requests
from firebase_admin import credentials, auth
from app.backend.services.auth_service.interfaces.user import User as UserInterface
from app.backend.services.auth_service.user import User
from requests.exceptions import HTTPError, ConnectionError, Timeout
from app.backend.services.auth_service.token import Token





class Auth:

    def __init__(self):
        self.api_key = "AIzaSyADwz7S2qrYj_vpp_v5iXtvPH_vioyahc4"
        self.auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"


    def register_user(self, email: str, password: str, username: str = None) -> UserInterface:
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=username,
            disabled=False
        )
        return User(user.uid, user.email, user.display_name)

    def authenticate(self, email: str, password: str) -> Token:
        try:
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            # Added a 10-second timeout for safety
            response = requests.post(self.auth_url, json=payload, timeout=10)
            
            # Parse early so we can use it in the error blocks
            data = response.json()
            
            # Manually trigger the HTTPError if status is 4xx/5xx
            response.raise_for_status()

            # Success path
            token = Token(data["idToken"])
            return token

        except Timeout:
            raise Exception("Authentication request timed out. Please try again.")
        except ConnectionError:
            raise Exception("Network error: Could not reach the auth server.")
        except HTTPError:
            error_msg = data.get("error", {}).get("message", "AUTH_FAILED") if data else "HTTP_ERROR"
            raise Exception(error_msg)
        except Exception as e:
            # Catch-all for unexpected issues
            raise Exception(f"An unexpected error occurred: {str(e)}")
        

    def verify_token(self, tokenString: str) -> Token:
        try:
            auth.verify_id_token(tokenString)
            return Token(tokenString=tokenString)
        except Exception as e:
            return False