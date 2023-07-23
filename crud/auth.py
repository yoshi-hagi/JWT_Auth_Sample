from fastapi import Depends, HTTPException
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from passlib.context import CryptContext
# 自作モジュール
from database import get_db
import models.auth as auth_model
import schema.auth as auth_schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 認証で使う、ユーザー名からデータ取得。一意になるはずなのでfirst()。authenticate_user関数で使うので一番上
async def get_user_by_name(db: AsyncSession, username:str) -> Optional[auth_model.User]:
    query = select(auth_model.User).filter(auth_model.User.username == username)
    result = await db.execute(query)
    return result.scalars().first()
# データの入力にはスキーマで定義した型を使い、データの処理はmodelで定義した方で処理する
async def create_new_user(db: AsyncSession, user_create: auth_schema.UserCreate) -> auth_model.User:
    # ユーザー名の重複チェック機能
    existing_user = await db.execute(select(auth_model.User).where(auth_model.User.username == user_create.username))
    existing_user = existing_user.scalars().first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="同名のユーザーが存在します")
    # 事前にデータを入れている場合は、idの最大値をとって+1の追加IDで入るようにする
    max_id = await db.execute(select(func.max(auth_model.User.id)))
    new_id = (max_id.scalar() or 0) + 1
    # パスワードをハッシュ値に変換するので個別の要素にする
    hashed_password = pwd_context.hash(user_create.password)
    new_user = auth_model.User(id=new_id, username=user_create.username, password=hashed_password, is_admin=user_create.is_admin)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
# 一覧なのでList-Tuple
async def get_all_users(db: AsyncSession) -> List[Tuple[auth_model.User]]:
    query = select(auth_model.User)
    result = await db.execute(query)
    return result.scalars().all()
# 選んだユーザーデータを修正・更新。is_adminの修正も出来るので管理者用
async def update_user_by_username4admin(db:AsyncSession, user_update:auth_schema.UserCreate, original:auth_model.User) -> auth_model.User:
    original.username = user_update.username
    original.password = pwd_context.hash(user_update.password)
    original.is_admin = user_update.is_admin
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original
# 選んだユーザーデータを修正・更新。ユーザー用
async def update_user_by_username4user(db:AsyncSession, user_update:auth_schema.UserUpdate, original:auth_model.User) -> auth_model.User:
    original.username = user_update.new_username
    original.password = pwd_context.hash(user_update.new_password)
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original
# データの削除。管理者・ユーザーの別はルーティング関数で行う
async def delete_user_by_username(db:AsyncSession, original:auth_model.User) -> None:
    await db.delete(original)
    await db.commit()