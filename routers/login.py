from fastapi import FastAPI, Request, Depends, status, HTTPException, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
# 自作モジュールのインポート
from auth.auth import get_current_user
from models.auth import User

# loginからサンプルコード表示に書き換え
router = APIRouter(tags=["login"])

templates = Jinja2Templates(directory="templates") # テンプレートがあるディレクトリを指定
# 認証用のトークンを発行するURLを指定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard")
async def read_dashboard(request: Request, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return templates.TemplateResponse("admin_dashboard.html", {"request": request, "username": current_user.username})
    else:
        return templates.TemplateResponse("user_dashboard.html", {"request": request, "username": current_user.username})
