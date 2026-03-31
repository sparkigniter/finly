from pydantic import BaseModel, EmailStr
from typing import Optional
class UserCreateDto(BaseModel) :
    username: Optional[str] = None
    email: EmailStr
    password: str
