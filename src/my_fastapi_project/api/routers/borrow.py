from fastapi import APIRouter

from my_fastapi_project.api.deps import BorrowServiceDep, CallerDep
from my_fastapi_project.schemas.borrow import BorrowRecordResponse

router = APIRouter(prefix="/borrows", tags=["borrows"])


@router.get(
    "/me",
    response_model=list[BorrowRecordResponse],
    summary="我的借阅记录",
)
async def my_borrows(caller: CallerDep, service: BorrowServiceDep):
    return await service.list_mine(caller["username"])
