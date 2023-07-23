from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# # DBの準備。非同期処理の場合はpostgresql+asyncpg:でURLを記述
# ASYNC_DB_URL = 'postgresql+asyncpg://yoshi:4491hag1wara@localhost:5432/xxxx'
# テスト用DBの準備。非同期処理の場合はsqlite+aiosqlite:でURLを記述
ASYNC_DB_URL = 'sqlite+aiosqlite:///db.sqlite3'

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_ = AsyncSession
)
# DBの宣言
Base = declarative_base()
# セッションを取得し、DBへアクセス
async def get_db():
    async with async_session() as session:
        yield session