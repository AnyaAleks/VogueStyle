from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from .request_model import RequestModel
from typing import List

class ServiceModel(Base):
    __tablename__ = "services"
    
    requests: Mapped[List['RequestModel']] = relationship()
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    time_minutes: Mapped[int] = mapped_column(Integer(), nullable=False)