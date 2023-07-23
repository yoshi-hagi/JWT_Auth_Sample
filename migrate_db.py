from sqlalchemy import create_engine
# 自作モジュール。modelで定義したデータベースの型をインポート
from models.auth import Base

# # テーブルの作成を行うだけなのでここでは非同期処理せず、通常の同期処理
# DB_URL = 'postgresql://yoshi:4491hag1wara@localhost:5432/xxxx'
# テスト用のSqliteデータベース
DB_URL = 'sqlite:///db.sqlite3'
engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    reset_database()