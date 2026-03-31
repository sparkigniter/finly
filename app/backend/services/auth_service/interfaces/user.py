from typing import Protocol

class User(Protocol):
    user_id: str
    email: str
    display_name: str


    def get_name(self) -> str:
        pass

    def get_email(self) -> str:
        pass

    def get_id(self) -> str:
        pass

    def set_token(self, token: str):
        pass

    def get_token(self) -> str:
        pass

    def set_refresh_token(self, refresh_token: str):
        pass

    def get_refresh_token(self) -> str:
        pass