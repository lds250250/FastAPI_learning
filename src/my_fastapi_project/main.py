import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


from my_fastapi_project.core.config import get_settings
from my_fastapi_project.api.routers.user import router as user_router
from my_fastapi_project.api.routers.health import router as health_router
from my_fastapi_project.api.routers.book import router as book_router

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


# ---------- 自定义中间件：给每个响应加耗时头 ----------


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    elapsed = (time.monotonic() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed:.0f}"
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
