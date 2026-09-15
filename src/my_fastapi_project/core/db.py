from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from my_fastapi_project.core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


class FakeSession:
    def __init__(self):
        print(">>> 打开会话")

    def ping(self) -> bool:
        return True

    def close(self) -> None:
        print(">>> 关闭会话")


async def get_session():
    session = FakeSession()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[FakeSession, Depends(get_session)]
