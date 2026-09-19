from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from my_fastapi_project.core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


def enable_sqlite_foreign_keys(async_engine: AsyncEngine) -> None:
    @event.listens_for(async_engine.sync_engine, "connect")
    def _enable(dbapi_connection, connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


if settings.DATABASE_URL.startswith("sqlite"):
    enable_sqlite_foreign_keys(engine)


class Base(DeclarativeBase):
    pass
