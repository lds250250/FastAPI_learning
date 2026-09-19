from fastapi import APIRouter
from sqlalchemy import text

from my_fastapi_project.api.deps import SessionDep

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="健康检查")
async def health_check():
    return {"status": "ok"}


@router.get("/db", summary="依赖连通性检查")
async def health_db(session: SessionDep):
    await session.execute(text("SELECT 1"))
    return {"database": "ok"}


#
