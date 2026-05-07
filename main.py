from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from databaseConn import SessionLocal
from models import User

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users