from fastapi import APIRouter, Body
from api.models.users import User, UserCreate
from api.models.messages import Message
import api.database.core as db
from typing import Union

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/users/", 
    response_description="Add new user",
    response_model=User,
    status_code=201,
    response_model_by_alias=False
)
async def create_user(user: User = Body(...)) -> dict[str, Union[User, str]]:
    try:
        db.users.insert_one(user.dict())
        return user
    except Exception as e:
        return {"error": str(e)}
    
    

@router.get("/messages/")
async def messages():
    with open("chat_log.txt", "r") as log_file:
        messages = log_file.readlines()
        messages = [msg.strip() for msg in messages if msg.strip()]
    return {"messages": messages}