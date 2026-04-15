"""Module providing client functionality."""
import os
from kiteconnect import KiteConnect


class KiteClient:
    """Client class to interact with the Kite Connect API."""

    def __init__(self):
        """Initializes a new instance of the class."""
        self.__api_key = os.getenv("KITE_API_KEY")
        self.__api_secret = os.getenv("KITE_API_SECRET")

    def get_client(self):
        """Retrieves the client."""
        kite = KiteConnect(api_key=self.__api_key)
        return kite

