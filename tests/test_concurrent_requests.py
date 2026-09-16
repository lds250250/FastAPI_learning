import asyncio
import time

import httpx

from my_fastapi_project.core.security import hash_password
from my_fastapi_project.main import app

CONCURRENT = 3
PASSWORD = "password123"


async def register_concurrently() -> tuple[float, list[int]]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        start = time.perf_counter()
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
        elapsed = time.perf_counter() - start
    return elapsed, [r.status_code for r in responses]


def test_concurrent_registrations_are_not_serialized(use_test_db):
    start = time.perf_counter()
    hash_password("calibration")
    single_hash = time.perf_counter() - start

    elapsed, statuses = asyncio.run(register_concurrently())

    assert statuses == [201] * CONCURRENT, f"状态码异常: {statuses}"
    assert elapsed < single_hash * 2, (
        f"{CONCURRENT} 个并发注册耗时 {elapsed:.3f}s，单次 bcrypt 约 {single_hash:.3f}s。"
        "接近 3 倍说明 bcrypt 阻塞了事件循环。"
    )
