from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ordo_storage.config import settings

async_engine = create_async_engine(settings.database_url, pool_pre_ping=True, echo=False)
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def check_database_connection() -> dict[str, str | bool]:
    async with async_engine.connect() as conn:
        version = (await conn.execute(text("SELECT version();"))).scalar_one()
        db_name = (await conn.execute(text("SELECT current_database();"))).scalar_one()
        return {
            "database": db_name,
            "version": version,
            "reachable": True,
        }
