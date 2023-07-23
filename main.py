from fastapi import FastAPI
# このほか、python-multipart、bcryptをインポート
# 自作モジュールのインポート
from routers import login
from routers import auth
from routers import token
from routers import api

app = FastAPI()
# メイン
app.include_router(login.router)
# JWT生成
app.include_router(token.router)
# 認証
app.include_router(auth.router)
# api用途
app.include_router(api.router)

if __name__ == '__main__':
    app.run()