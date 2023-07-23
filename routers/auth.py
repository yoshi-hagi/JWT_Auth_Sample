from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
# 自作モジュール
from database import get_db
import schema.auth as auth_schema
import crud.auth as auth_crud
import auth.auth as auth_func

router = APIRouter(tags=["auth"])

## ここではauthのcrudを取り扱う
# 新規データ作成。管理者用
@router.post('/auth/create/admin', response_model=auth_schema.UserCreateResponse)
async def create_new_user(
    user_body: auth_schema.UserCreate, db:AsyncSession = Depends(get_db),
    user = Depends(auth_func.get_current_user)
    ): # 管理者認証
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理者のみリクエストが可能です。",
        )
    return await auth_crud.create_new_user(db, user_body)
# 新規データ作成。ユーザー用
@router.post('/auth/create/user', response_model=auth_schema.UserCreateResponse)
async def create_new_user(user_body: auth_schema.UserCreate, db:AsyncSession = Depends(get_db)):
    # UserCreateスキーマを利用しつつ、is_adminはFalseに書き換える
    # user_body.is_admin = False # 管理者権限を付与させない場合は#を外す
    return await auth_crud.create_new_user(db, user_body)
# 全データ取得。管理者のみ
@router.get('/auth/read/all', response_model=List[auth_schema.UserCreateResponse])
async def user_all(db:AsyncSession = Depends(get_db),
    user = Depends(auth_func.get_current_user)
    ): # 管理者認証
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理者のみリクエストが可能です。",
        )
    return await auth_crud.get_all_users(db)
# 選択したデータの更新。管理者Ver
@router.put('/auth/update/admin', response_model=auth_schema.UserCreateResponse)
async def update_user4admin(
    update_user:str, update_data:auth_schema.UserCreate,
    db:AsyncSession = Depends(get_db), user = Depends(auth_func.get_current_user)
    ):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理者のみリクエストが可能です。",
        )
    user = await auth_crud.get_user_by_name(db, username=update_user) # 別のユーザーデータの変更を想定
    if user is None:
        raise HTTPException(status_code=404, detail="指定したユーザー名のデータは存在しません")
    return await auth_crud.update_user_by_username4admin(db, update_data, original=user)
# 選択したデータの更新。ユーザーVer。スキーマではなく個別のusernameとpasswordを渡す
@router.put('/auth/update/user', response_model=auth_schema.UserCreateResponse)
async def update_user4user(user_update:auth_schema.UserUpdate,db:AsyncSession = Depends(get_db), user = Depends(auth_func.get_current_user)):
    user = await auth_crud.get_user_by_name(db, username=user.username) # ユーザー自身のデータ変更のため、認証ユーザー名をとる
    if user is None:
        raise HTTPException(status_code=404, detail="指定したユーザー名のデータは存在しません")
    return await auth_crud.update_user_by_username4user(db, user_update, original=user)
# 選択したデータの削除。管理者Ver
@router.delete('/user/delete/admin', response_model=None)
async def delete_user4admin(
    delete_user:str, db:AsyncSession = Depends(get_db), user = Depends(auth_func.get_current_user)
    ):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理者のみリクエストが可能です。",
        )
    delete_data = await auth_crud.get_user_by_name(db, username=delete_user) # 別のユーザーデータの変更を想定
    if delete_data is None:
        raise HTTPException(status_code=404, detail="指定したIDデータは存在しません")
    return await auth_crud.delete_user_by_username(db, original=delete_data)
# 選択したデータの削除。ユーザーVer。
@router.delete('/user/delete/user', response_model=None)
async def delete_user4admin(db:AsyncSession = Depends(get_db), user = Depends(auth_func.get_current_user)):
    delete_user = await auth_crud.get_user_by_name(db, username=user.username) # ユーザー自身のデータ変更のため、認証ユーザー名をとる
    if delete_user is None:
        raise HTTPException(status_code=404, detail="指定したユーザー名のデータは存在しません")
    return await auth_crud.delete_user_by_username(db, original=delete_user)