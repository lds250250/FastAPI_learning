import asyncio
import threading

import httpx

from my_fastapi_project.core.security import hash_password
from my_fastapi_project.main import app

CONCURRENT = 3
PASSWORD = "password123"


async def register_concurrently() -> list[int]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        responses = await asyncio.gather(
            *(
                client.post(
                    "/users/register/",
                    json={
                        "username": f"concurrent{i}",
                        "email": f"concurrent{i}@example.com",
                        "password": PASSWORD,
                    },
                )
                for i in range(CONCURRENT)
            )
        )
    return [r.status_code for r in responses]


def test_password_hashing_runs_off_the_event_loop(use_test_db, monkeypatch):
    """bcrypt 必须在别的线程里跑 —— 在主线程里跑会卡住整个事件循环。"""
    seen: list[int] = []
    real_hash = hash_password

    def spy(password: str) -> str:
        seen.append(threading.get_ident())
        return real_hash(password)

    monkeypatch.setattr("my_fastapi_project.services.user_service.hash_password", spy)

    statuses = asyncio.run(register_concurrently())

    assert statuses == [201] * CONCURRENT
    assert len(seen) == CONCURRENT
    assert all(tid != threading.main_thread().ident for tid in seen)
