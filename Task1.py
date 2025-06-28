from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID
from typing import Dict

app = FastAPI()

# In-memory storage
users: Dict[UUID, dict] = {}

# User schema
class User(BaseModel):
    name: str
    email: EmailStr
    age: int

# ==============================
# 🔸 Create a new user
# ==============================
@app.post("/users", status_code=201)
def create_user(user: User):
    user_id = uuid4()
    users[user_id] = user.dict()
    return {"id": user_id, **user.dict()}

# ==============================
# 🔹 Get a user by ID
# ==============================
@app.get("/users/{user_id}")
def get_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **users[user_id]}

# ==============================
# 🔄 Update a user
# ==============================
@app.put("/users/{user_id}")
def update_user(user_id: UUID, updated_user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = updated_user.dict()
    return {"id": user_id, **updated_user.dict()}

# ==============================
# ❌ Delete a user
# ==============================
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return
