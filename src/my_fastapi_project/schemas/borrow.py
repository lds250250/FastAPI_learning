from datetime import datetime

from pydantic import BaseModel, Field


class BorrowRecordResponse(BaseModel):
    id: int = Field(..., description="借阅记录编号")
    isbn: str = Field(..., description="图书 ISBN")
    title: str = Field(..., description="书名")
    borrowed_at: datetime = Field(..., description="借出时间")
    returned_at: datetime | None = Field(None, description="归还时间，未还则为空")
