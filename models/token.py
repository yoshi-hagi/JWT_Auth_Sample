from pydantic import BaseModel

class TokenData(BaseModel):
    username: str = None
    is_admin: bool = False  # boolで管理者か否かを判定
    
class Token(TokenData):
    access_token: str
    token_type: str
