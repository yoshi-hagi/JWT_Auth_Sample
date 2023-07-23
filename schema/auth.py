from pydantic import BaseModel, Field, validator

# 認証で使う変数
class User(BaseModel):
    username: str = Field(None, description='ユーザー認証名')
    
    @validator("username")
    def check_user(user):
        if user.encode('utf-8').isalnum() == False:
            raise ValueError("ユーザー名は半角英数字のみ使用してください")
        return user
    
# パスワードはAPIのレスポンスに含めず、Create用のクラスに付加
class UserCreate(User):
    password: str = Field(None, description='パスワード')
    is_admin: bool = Field(False, description='管理者か否か')

# CRUDデータ型。データベースに追加するためのID、sqlalchemyで使うためのORMモードを設定
class UserCreateResponse(UserCreate):
    id: int = Field(None, description='ユーザーの登録ID。自動採番')
    class Config:
        orm_mode = True

# ユーザー自身がユーザー名とパスワードを更新するためのスキーマ
class UserUpdate(BaseModel):
    new_username: str = Field(None, description='新しいユーザー名')
    new_password: str = Field(None, description='新しいパスワード')

    @validator("new_username")
    def check_user(cls, new_username):
        if new_username.encode('utf-8').isalnum() == False:
            raise ValueError("ユーザー名は半角英数字のみ使用してください")
        return new_username
