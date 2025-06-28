
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, new_data: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = new_data.name
        user.email = new_data.email
        user.age = new_data.age
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
