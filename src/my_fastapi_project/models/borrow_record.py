from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_fastapi_project.core.db import Base
from my_fastapi_project.models.book import Book
from my_fastapi_project.models.user import User


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), ForeignKey("users.username"))
    isbn: Mapped[str] = mapped_column(String(13), ForeignKey("books.isbn"))
    borrowed_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    returned_at: Mapped[datetime | None] = mapped_column()

    user: Mapped[User] = relationship()
    book: Mapped[Book] = relationship()
