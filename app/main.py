from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Docker User Management API")

# Simple in-memory storage mimicking a database for your assignment steps
users_db: Dict[int, dict] = {}
id_counter = 1

class UserCreate(BaseModel):
    name: str
    surname: str

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str

@app.post("/users/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate):
    global id_counter
    new_user = {"id": id_counter, "name": user.name, "surname": user.surname}
    users_db[id_counter] = new_user
    id_counter += 1
    return new_user

@app.get("/users", response_model=List[UserResponse])
def list_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)
def edit_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].update({"name": user.name, "surname": user.surname})
    return users_db[user_id]

@app.delete("/users/{user_id}")
def remove_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}