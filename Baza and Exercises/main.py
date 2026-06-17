import sys
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse # <-- DODANO do strumieniowania wideo
from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
from typing import List
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv

# --- KONFIGURACJA ŚCIEŻEK (Aby Python widział folder Exercises) ---
# Dodajemy folder 'Exercises' do ścieżek systemowych Pythona
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Exercises')))

import biceps
import barki
import wyskok

from database import SessionLocal
from models import User, Exercise, Stats
import data

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Brak SECRET_KEY w pliku .env!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Konfiguracja szyfrowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# --- MIDDLEWARE (Niezbędne do połączenia z frontendem) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- HELPERY KRYPTOGRAFICZNE ---
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --- HELPERY JWT ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"\n--- DEBUG: Otrzymany token: {token[:20]}... ---")
    try:
        # Używamy krotki ("HS256",)
        payload = jwt.decode(token, SECRET_KEY, algorithms=("HS256",))
        print(f"--- DEBUG: Zdekodowany payload: {payload} ---")
        
        user_id_str = payload.get("sub")
        if user_id_str is None:
            print("--- DEBUG: BŁĄD - Brak pola 'sub' w tokenie! ---")
            raise HTTPException(status_code=401, detail="Nieprawidłowy token")
            
        user_id = int(user_id_str)
        
    except jwt.ExpiredSignatureError:
        print("--- DEBUG: BŁĄD - Token wygasł! ---")
        raise HTTPException(status_code=401, detail="Sesja wygasła, zaloguj się ponownie")
    except jwt.PyJWTError as e:
        print(f"--- DEBUG: BŁĄD DEKODOWANIA JWT: {e} ---")
        raise HTTPException(status_code=401, detail="Błąd autoryzacji tokena")
    
    user = db.query(User).filter(User.UserID == user_id).first()
    if user is None:
        print(f"--- DEBUG: BŁĄD - Nie znaleziono w bazie użytkownika o ID {user_id} ---")
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")
    
    print(f"--- DEBUG: Autoryzacja udana! Użytkownik: {user.Nickname} ---")
    return user


# --- ENDPOINTY UŻYTKOWNIKA ---
@app.post("/register", response_model=data.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: data.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(or_(User.Nickname == user_data.Nickname, User.Email == user_data.Email)).first():
        raise HTTPException(status_code=400, detail="Użytkownik o takim Nicku lub Emailu już istnieje")

    hashed_pwd = hash_password(user_data.Password)
    user_dict = user_data.model_dump()
    user_dict["Password"] = hashed_pwd

    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(login_data: data.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        or_(User.Email == login_data.Login, User.Nickname == login_data.Login)
    ).first()

    if not user or not verify_password(login_data.Password, user.Password):
        raise HTTPException(status_code=401, detail="Błędne dane logowania")

    access_token = create_access_token(data={"sub": str(user.UserID)})
    return {"access_token": access_token, "token_type": "bearer", "user": user.Nickname}


@app.post("/logout")
def logout():
    return {"message": "Wylogowano"}


# --- ENDPOINTY TRENINGOWE (CyberTrainer Logic) ---
@app.get("/exercises", response_model=List[data.ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).all()


@app.post("/stats", status_code=status.HTTP_201_CREATED)
def add_workout_result(
    stats: data.StatsCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_stat = Stats(
        IDUser=current_user.UserID,
        **stats.model_dump()
    )
    db.add(new_stat)
    db.commit()
    return {"status": "success", "detail": "Wynik zapisany"}


@app.get("/stats/me")
def get_my_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(Stats).filter(Stats.IDUser == current_user.UserID).all()
    return results

@app.post("/api/save-stats")
def save_workout_results(
    stats_data: data.StatsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_stat = Stats(
        IDUser=current_user.UserID,
        IDExercise=stats_data.IDExercise,
        RepCount=stats_data.RepCount,
        Weight=stats_data.Weight,
        JumpHeight=stats_data.JumpHeight
    )

    db.add(new_stat)
    db.commit()
    db.refresh(new_stat)

    return{"status": "success", "detail": "Wynik zapisany pomyślnie"}

# --- ENDPOINTY KAMER (MediaPipe) ---
@app.get("/api/video-stream/{exercise_id}")
def start_exercise(exercise_id: str):
    if exercise_id == "1":
        return StreamingResponse(biceps.generuj_obraz_biceps(), media_type="multipart/x-mixed-replace; boundary=frame")
    elif exercise_id == "2":
        return StreamingResponse(barki.generuj_obraz_barki(), media_type="multipart/x-mixed-replace; boundary=frame")
    elif exercise_id == "3":
        return StreamingResponse(wyskok.generuj_obraz_wyskok(), media_type="multipart/x-mixed-replace; boundary=frame")
    
@app.post("/api/stop-exercise/{exercise_id}")
def stop_exercise(exercise_id: int):
    # Domyślne wartości
    wynik_powtorzenia = 0
    wynik_dodatkowy = 0.0 # Będzie to jumpHeight dla skoków
    
    if exercise_id == 1:
        wynik_powtorzenia = biceps.zatrzymaj_trening()
        
    elif exercise_id == 2:
        wynik_powtorzenia = barki.zatrzymaj_trening()
        
    elif exercise_id == 3:
        # Teraz tutaj odbieramy słownik z wyskok.py
        dane_wyskok = wyskok.zatrzymaj_trening() 
        wynik_powtorzenia = dane_wyskok["powtorzenia"]
        wynik_dodatkowy = dane_wyskok["jumpHeight"]

    # Zwracamy spójny obiekt JSON, który łatwo odczytasz w React
    return {
        "status": "success", 
        "powtorzenia": wynik_powtorzenia, 
        "jumpHeight": wynik_dodatkowy
    }