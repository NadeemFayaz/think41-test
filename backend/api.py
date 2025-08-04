from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_creation import Base, User
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Create DB engine once at startup instead of on each request
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response
class UserCreate(BaseModel):
    first_name: str
    email: str
    password: str  # In real app, you'd want to hash this

class UserResponse(BaseModel):
    id: int
    first_name: str
    email: str

# Seed initial test data
@app.post("/seed-data", status_code=status.HTTP_201_CREATED)
def seed_data(db: Session = Depends(get_db)):
    # Only seed if no users exist
    if db.query(User).count() == 0:
        test_users = [
            User(first_name="Alice", email="alice@example.com", password="password123"),
            User(first_name="Bob", email="bob@example.com", password="password456")
        ]
        db.add_all(test_users)
        db.commit()
    return {"message": "Test data created"}

@app.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}", response_model=Optional[UserResponse])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(first_name=user.first_name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user