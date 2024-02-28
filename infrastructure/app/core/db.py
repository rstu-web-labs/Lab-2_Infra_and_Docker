from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings

Base = type("Base", (AsyncAttrs, DeclarativeBase), {})
engine = create_async_engine(settings.postgres_database_url)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


async def check_db_connection() -> bool:
    async with AsyncSessionLocal() as session:
        try:
            return bool(await session.execute(text("SELECT 1")))
        except Exception as error:
            logger.critical(f"Postgres connection error: {error}", exc_info=True)
            return False
