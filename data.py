from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    Nickname: str = Field(..., min_length=3, max_length=50)
    Age: int = Field(..., gt=0, lt=120)
    IDGender: int
    IDAdvancement: int
    Email: EmailStr = Field(..., max_length=50)
    Password: str = Field(..., min_length=8, max_length=30)

class UserResponse(BaseModel):
    UserID: int
    Nickname: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    Login: str
    Password : str