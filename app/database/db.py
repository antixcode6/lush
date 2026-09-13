import os
from pathlib import Path
from typing import AsyncIterator
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    event,
    text,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.database.base import Base
from app.database import models


DATA_DIR = Path(
    os.getenv("DATA_DIR", Path(__file__).resolve().parent.parent.parent / "data")
)
DB_PATH = DATA_DIR / "main.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")


# Enable foreign keys on every new DBAPI connection.
@event.listens_for(engine.sync_engine, "connect")
def _enable_sqlite_fk(dbapi_conn, _record):
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.close()


AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def setup_db() -> None:
    """Create tables/indexes if they don't already exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI-style dependency that yields an AsyncSession."""
    async with AsyncSessionLocal() as session:
        yield session
