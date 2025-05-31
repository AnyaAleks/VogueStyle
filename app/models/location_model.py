from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

if TYPE_CHECKING:
    # Для подсказок типов в IDE/mypy, но не используется при рантайм-импорте
    from .master_model import MasterModel

class LocationModel(Base):
    __tablename__ = "locations"

    # Не импортируем MasterModel «боевым» путём, используем строку для relationship
    masters: Mapped[List["MasterModel"]] = relationship("MasterModel", back_populates="location")

    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
