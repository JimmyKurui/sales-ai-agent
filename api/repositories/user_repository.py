from fastapi import Depends
from bson import ObjectId
from pymongo.errors import PyMongoError
from api.database.mongodb import get_db
from api.models.user import UserInDB
from typing import Optional



class UserRepository:
    def __init__(self):
        self.collection = get_db().users
        
    async def get_user(self, username: str) -> UserInDB:
        try:
            user = await self.collection.find_one({"username": username})
            if user:
                return UserInDB(**user)
        except PyMongoError as e:
            raise Exception(f"An error occured: {e}")
        
    async def create_user(self, user: UserInDB) -> UserInDB:
        try:
            result = await self.collection.insert_one(user.model_dump())
            if result.acknowledged:
                user.id = str(result.inserted_id)
                return user
        except PyMongoError as e:
            raise Exception(f"An error occured: {e}")
        
    async def update_password(self, user_id: str, password: str) -> bool:
        try:
            result = await self.collection.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": password}}
            )
            return bool(result.acknowledged)
        except PyMongoError as e: 
            raise Exception(f"An error occured: {e}")
                
    async def update_user(self, user_id: str, updated_user: UserInDB) -> Optional[UserInDB]:
        try:
            result = await self.collection.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {**updated_user.model_dump_json()}}
            )
            if not result.acknowledged:
                return None
            return UserInDB(**updated_user)
        except PyMongoError as e:
            raise Exception(f"An error occured: {e}")