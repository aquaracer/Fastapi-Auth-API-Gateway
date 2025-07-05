from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from src.config.database.database import Base


class User(Base):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    yandex_access_token: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
