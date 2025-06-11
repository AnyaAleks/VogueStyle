from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class TgModel(Base):
    __tablename__ = "tg"

    tg_id: Mapped[int] = mapped_column(unique=True)
    role: Mapped[int]
