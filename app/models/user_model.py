from __future__ import annotations
from datetime import date
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date
from .base_model import Base

if TYPE_CHECKING:
    from .request_model import RequestModel

class UserModel(Base):
    __tablename__ = "users"

    requests: Mapped[List["RequestModel"]] = relationship("RequestModel", back_populates="user")

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(30), nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    tg_id: Mapped[int] = mapped_column(Integer(), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
