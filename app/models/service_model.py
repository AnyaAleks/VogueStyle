from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Integer
from .base_model import Base
from .servicemaster_model import services_masters

if TYPE_CHECKING:
    from .request_model import RequestModel
    from .master_model import MasterModel

class ServiceModel(Base):
    __tablename__ = "services"
    
    masters: Mapped[List["MasterModel"]] = relationship("MasterModel", secondary=services_masters, back_populates="services")
    requests: Mapped[List["RequestModel"]] = relationship("RequestModel", back_populates="service")

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    time_minutes: Mapped[int] = mapped_column(Integer(), nullable=False)

    @validates("master_id")
    def validate_masterId(self, key, value):
        if value < 0:
            raise ValueError(f"Incorrect master_id: {value}")
        return value
