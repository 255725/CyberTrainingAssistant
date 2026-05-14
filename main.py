from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
from typing import List

from databaseConn import SessionLocal
from models import User, Exercise, Stats
import data

# Konfiguracja szyfrowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# --- MIDDLEWARE (Niezbędne do połączenia z frontendem) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji podaj konkretny adres strony
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tymczasowa sesja (w przyszłości zastąpimy to tokenem JWT)
current_active_user = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- HELPERY ---
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --- ENDPOINTY UŻYTKOWNIKA ---

@app.post("/register", response_model=data.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: data.UserCreate, db: Session = Depends(get_db)):
    # Sprawdzanie czy nick/email wolny
    if db.query(User).filter(or_(User.Nickname == user_data.Nickname, User.Email == user_data.Email)).first():
        raise HTTPException(status_code=400, detail="Użytkownik o takim Nicku lub Emailu już istnieje")

    # Szyfrowanie hasła przed zapisem
    hashed_pwd = hash_password(user_data.Password)

    # Tworzenie obiektu (wykluczamy surowe hasło, wstawiamy zahashowane)
    user_dict = user_data.model_dump()
    user_dict["Password"] = hashed_pwd

    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(login_data: data.LoginRequest, db: Session = Depends(get_db)):
    global current_active_user

    user = db.query(User).filter(
        or_(User.Email == login_data.Login, User.Nickname == login_data.Login)
    ).first()

    if not user or not verify_password(login_data.Password, user.Password):
        raise HTTPException(status_code=401, detail="Błędne dane logowania")

    current_active_user = user
    return {"message": "Zalogowano", "user": user.Nickname}


@app.post("/logout")
def logout():
    global current_active_user
    current_active_user = None
    return {"message": "Wylogowano"}


# --- ENDPOINTY TRENINGOWE (CyberTrainer Logic) ---

@app.get("/exercises", response_model=List[data.ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).all()


@app.post("/stats", status_code=status.HTTP_201_CREATED)
def add_workout_result(stats: data.StatsCreate, db: Session = Depends(get_db)):
    if not current_active_user:
        raise HTTPException(status_code=401, detail="Musisz być zalogowany")

    new_stat = Stats(
        IDUser=current_active_user.UserID,
        **stats.model_dump()
    )
    db.add(new_stat)
    db.commit()
    return {"status": "success", "detail": "Wynik zapisany"}


@app.get("/stats/me")
def get_my_history(db: Session = Depends(get_db)):
    if not current_active_user:
        raise HTTPException(status_code=401, detail="Zaloguj się")

    # Pobieranie wyników zalogowanego usera
    results = db.query(Stats).filter(Stats.IDUser == current_active_user.UserID).all()
    return results