from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Rejestracja
class UserCreate(BaseModel):
    Nickname: str = Field(..., min_length=3, max_length=50)
    Age: int = Field(..., gt=0, lt=120)
    IDGender: int
    IDAdvancement: int
    Email: EmailStr
    Password: str = Field(..., min_length=8)

# Odpowiedź (bez hasła!)
class UserResponse(BaseModel):
    UserID: int
    Nickname: str
    Email: str
    Age: int

    class Config:
        from_attributes = True

# Logowanie
class LoginRequest(BaseModel):
    Login: str  # Tu wpisujemy Nickname lub Email
    Password: str

# Dodawanie statystyk treningu
class StatsCreate(BaseModel):
    IDExercise: int
    RepCount: int
    Weight: float
    JumpHeight: float

class ExerciseResponse(BaseModel):
    ExerciseID: int
    ExerciseName: str
    class Config:
        from_attributes = True