from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.errors import PyMongoError
from datetime import timedelta
from bson import ObjectId

from api.auth.session import (
    get_user,
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password
)
from api.models.users import User, UserInDB, Token, PasswordChange
from api.database.mongodb import get_db


router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register(user: UserInDB = Body(...)) -> User:
    try:
        db = await get_db()
        current_user = await get_user(db, user.username)
        if current_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registered",
            )
        user.password = get_password_hash(user.password.get_secret_value())
        result = await db.users.insert_one(user.model_dump())
        user.id = str(result.inserted_id)
        if not result.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed"
            )
        return User(**user.model_dump())
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = await get_db()
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles}
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/change-password", response_model=User)
async def change_password(
    password_data: PasswordChange = Body(...),
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        if not verify_password(password_data.current_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect"
            )
        if password_data.current_password == password_data.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from the current password"
            )
        if password_data.current_password == password_data.confirm_password or password_data.new_password != password_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from the current password"
            )
        db = await get_db()
        new_hashed = get_password_hash(password_data.new_password)
        await db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {"password": new_hashed}}
        )
        current_user.password = new_hashed
        return User(**current_user.model_dump())
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user