import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from my_fastapi_project.api import ws_bus
from my_fastapi_project.api.routers.auth import router as auth_router
from my_fastapi_project.api.routers.book import router as book_router
from my_fastapi_project.api.routers.borrow import router as borrow_router
from my_fastapi_project.api.routers.health import router as health_router
from my_fastapi_project.api.routers.user import router as user_router
from my_fastapi_project.api.routers.ws import router as ws_router
from my_fastapi_project.core.config import get_settings
from my_fastapi_project.core.db import engine
from my_fastapi_project.core.errors import register_exception_handlers
from my_fastapi_project.core.logging_config import request_id_var, setup_logging
from my_fastapi_project.core.redis import redis_client

settings = get_settings()

setup_logging()


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(ws_bus.subscribe_loop(redis_client))
    logger.info("应用启动")

    yield

    logger.info("应用关闭中")

    task.cancel()
    with suppress(asyncio.CancelledError):
        await task

    await redis_client.aclose()
    await engine.dispose()

    logger.info("应用已关闭")


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

app.include_router(auth_router)

register_exception_handlers(app)


# ---------- 请求日志中间件 ----------


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.monotonic()

    logger.info("→ %s %s", request.method, request.url.path)

    response = await call_next(request)

    elapsed = (time.monotonic() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed:.0f}"
    logger.info(
        "← %s %s → %s  %.0f ms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex
    request.state.request_id = rid
    request_id_var.set(rid)

    response = await call_next(request)

    response.headers["X-Request-ID"] = rid
    return response


# ---------- CORS ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(health_router)
app.include_router(book_router)
app.include_router(borrow_router)
app.include_router(ws_router)
