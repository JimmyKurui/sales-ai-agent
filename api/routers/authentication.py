from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import logging

from api.config.session import (
    create_user,
    get_current_user,
    authenticate_user,
    create_access_token,
    change_current_password,
)
from api.models.user import User, UserInDB, Token, PasswordChange



router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register(user: UserInDB = Body(...)) -> User:
    try:
        user = await create_user(user)
        if not user:
            logging.error(f"User registration failed for: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed"
            )
        return user
    except Exception as e:
        logging.exception(f"User registration failed for: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occured: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            logging.error(f"Incorrect username or password for: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": user.username, "roles": user.roles}
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        logging.exception(f"Login failed for: {user.username}")
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Login failed: {str(e)}"
            )

@router.post("/change-password", response_model=User)
async def change_password(
    password_data: PasswordChange = Body(...),
    current_user: UserInDB = Depends(get_current_user)
):
    if change_current_password(password_data):
        return User(**current_user.model_dump())
    else:
        logging.error(f"Could not change password for {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occured while changing password"
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user