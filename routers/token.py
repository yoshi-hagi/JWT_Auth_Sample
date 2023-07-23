from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
# 自作モジュール
from database import get_db
import models.token as token_models
import auth.auth as auth_func

router = APIRouter(tags=["token"])

@router.post("/token", response_model=token_models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await auth_func.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名かパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_func.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =  await auth_func.create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin}
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username, "is_admin": user.is_admin}