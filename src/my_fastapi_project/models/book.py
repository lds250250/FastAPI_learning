from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from my_fastapi_project.core.db import Base


class Book(Base):
    __tablename__ = "books"

    isbn: Mapped[str] = mapped_column(String(13), primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column()
    internal_note: Mapped[str | None] = mapped_column(String(200))
