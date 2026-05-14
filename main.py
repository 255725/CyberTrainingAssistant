from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from databaseConn import SessionLocal
from models import User
import data


app = FastAPI()

current_active_user = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/register", response_model=data.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: data.UserCreate, db: Session = Depends(get_db)):
    db_nickname = db.query(User).filter(User.Nickname == user_data.Nickname).first()
    db_email = db.query(User).filter(User.Email == user_data.Email).first()
    if db_nickname:
        raise HTTPException(status_code=400, detail="Podany nick jest już zajęty")

    if db_email:
        raise HTTPException(status_code=400, detail="Konto już istnieje")

    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(login_data: data.LoginRequest, db: Session = Depends(get_db)):
    global current_active_user

    user = db.query(User).filter(
        or_(
            User.Email == login_data.Login,
            User.Nickname == login_data.Login
        )
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Tutaj docelowo dojdzie jeszcze weryfikacja hasła
    if user.Password != login_data.Password:
        raise HTTPException(status_code=401, detail="Invalid password")

    current_active_user = user
    return {"message": f"Logged in as {user.Nickname}", "user_id": user.UserID}

@app.get("/me", response_model=data.UserResponse)
def get_current_user():
    if not current_active_user:
        raise HTTPException(status_code=401, detail="Not logged in")
    return current_active_user
