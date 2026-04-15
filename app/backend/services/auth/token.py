"""Token.py"""

import jwt


class Token:
    """A simple wrapper around JWT tokens to provide easy access to claims and metadata."""

    def __init__(self, token_string: str):
        """Initializes a new instance of the class."""
        self.token_string = token_string
        self.decoded_token = self.decode()

    def decode(self) -> dict:
        """Decodes the payload without verifying the signature (for reading data)."""
        try:
            return jwt.decode(
                self.token_string, options={
                    "verify_signature": False})
        except Exception:
            # Returns an empty dict if the string isn't a valid JWT format
            return {}

    # --- STANDARD JWT CLAIM GETTERS ---

    def get_subject(self) -> str:
        """The User ID (UID)."""
        return self.decoded_token.get("sub")

    def get_expiry(self) -> int:
        """Expiration time (Unix timestamp)."""
        return self.decoded_token.get("exp")

    def get_issued_at(self) -> int:
        """Time the token was issued (Unix timestamp)."""
        return self.decoded_token.get("iat")

    def get_issuer(self) -> str:
        """The issuer of the token (e.g., 'https://securetoken.google.com/your-project-id')."""
        return self.decoded_token.get("iss")

    def get_audience(self) -> str:
        """The intended audience for the token (e.g., your Firebase project ID)."""
        return self.decoded_token.get("aud")

    def get_not_before(self) -> int:
        """The time before which the token is not valid (Unix timestamp)."""
        return self.decoded_token.get("nbf")

    def get_id(self) -> str:
        """JWT ID (a unique identifier for the token)."""
        return self.decoded_token.get("jti")

    # --- HEADER / METADATA GETTERS ---

    def get_header(self) -> dict:
        """Extracts the header (alg, kid, typ) from the token string."""
        try:
            return jwt.get_unverified_header(self.token_string)
        except BaseException:
            return {}

    def get_algorithm(self) -> str:
        """Retrieves the algorithm."""
        return self.get_header().get("alg")

    def get_key_id(self) -> str:
        """Retrieves the key id."""
        return self.get_header().get("kid")

    # --- CUSTOM CLAIMS HELPERS ---

    def get_claims(self) -> dict:
        """Returns the full payload dictionary."""
        return self.decoded_token

    def get_claim(self, key: str, default=None):
        """
        Safely fetches a specific claim (like 'role' or 'premium').
        Returns the default value if the key is missing.
        """
        return self.decoded_token.get(key, default)

    def has_claim(self, key: str) -> bool:
        """Checks if a specific claim exists in the payload."""
        return key in self.decoded_token

    # --- VERIFICATION METHODS ---

    def verify_signature(self, secret: str, algorithm: str = "HS256") -> bool:
        """Verifies the signature using a local secret key (Symmetric)."""
        try:
            jwt.decode(self.token_string, secret, algorithms=[algorithm])
            return True
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.InvalidTokenError):
            return False

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the token, including the token string and its expiry."""
        return {
            "tokenString": self.token_string,
            "expires_at": self.get_expiry()}

