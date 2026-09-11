from typing import Annotated

from fastapi import Depends


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
