
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: str, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, updated_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
