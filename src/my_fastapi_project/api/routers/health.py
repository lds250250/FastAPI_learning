from fastapi import APIRouter

from my_fastapi_project.core.db import SessionDep

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="健康检查")
async def health_check():
    return {"status": "ok"}


@router.get("/db", summary="依赖连通性检查")
async def health_db(session: SessionDep):
    return {"database": "ok" if session.ping() else "down"}
