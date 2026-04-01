"""Data Transfer Object (DTO) for creating a new user in the system."""
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreateDto(BaseModel):
    """DTO for user registration."""
    username: Optional[str] = None
    email: EmailStr
    password: str
