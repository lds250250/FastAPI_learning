from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from my_fastapi_project.core.db import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(60))
    role: Mapped[str] = mapped_column(String(20))
    profile: Mapped[dict | None] = mapped_column(JSON)
