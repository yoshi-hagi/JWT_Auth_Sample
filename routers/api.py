from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
# 自作モジュール
from database import get_db
import schema.auth as auth_schema
import crud.auth as auth_crud
import auth.auth as auth_func

router = APIRouter(tags=["api"])

# 管理者は全ユーザー、ユーザーは自身のデータを取得する
@router.get('/userdata', response_model=List[auth_schema.UserCreateResponse])
async def user_data(db:AsyncSession = Depends(get_db),
    user = Depends(auth_func.get_current_user)
    ): # 管理者の時はユーザーの全データ取得
    if user.is_admin:
        return await auth_crud.get_all_users(db)
    else:
        userdata = await auth_crud.get_user_by_name(db, username=user.username)
        return [userdata] # リストとして返している