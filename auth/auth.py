from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from jose import JWTError, jwt # python-joseをインポート
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
# 自作モジュール
from database import get_db
import models.auth as auth_models
import crud.auth as auth_crud
import models.token as token_models

# 各変数
SECRET_KEY = "YOUR-SECRET-KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ユーザー認証
async def authenticate_user(username: str, password: str, db:AsyncSession = Depends(get_db)):
    user = await auth_crud.get_user_by_name(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

# トークンの生成
async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# トークンからのユーザーデータの照合
async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # トークンからデータの抽出
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        if username is None:
            raise credentials_exception
        token_data = token_models.TokenData(username=username, is_admin=is_admin)
    except JWTError:
        raise credentials_exception

    stmt = select(auth_models.User).where(auth_models.User.username == token_data.username)
    result = await db.execute(stmt)
    user = result.scalar()

    if user is None:
        raise credentials_exception
    return user

