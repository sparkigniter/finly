"""Data Transfer Object (DTO) for user login credentials."""
from pydantic import BaseModel


class LoginDto(BaseModel):
    """DTO for user login."""
    email: str
    password: str
