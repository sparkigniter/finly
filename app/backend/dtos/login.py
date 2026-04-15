"""Data Transfer Object (DTO) for user login credentials."""

from pydantic import BaseModel, EmailStr, Field


class LoginDto(BaseModel):
    """DTO for user login with validated email and password."""

    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters long"
    )
