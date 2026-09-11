import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from my_fastapi_project.api.routers.book import router as book_router
from my_fastapi_project.api.routers.health import router as health_router
from my_fastapi_project.api.routers.user import router as user_router
from my_fastapi_project.core.config import get_settings
from my_fastapi_project.core.errors import register_exception_handlers

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

register_exception_handlers(app)


# ---------- 请求日志中间件 ----------


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.monotonic()

    response = await call_next(request)

    elapsed = (time.monotonic() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed:.0f}"
    rid = getattr(request.state, "request_id", "-")
    print(
        f"[{rid}][{request.method}] {request.url.path} "
        f"→ {response.status_code}  {elapsed:.0f} ms"
    )
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex
    request.state.request_id = rid

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
