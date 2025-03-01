from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime as dt

class RequestModel(Base):
    __tablename__ = "requests"
    
    master: Mapped[int] = mapped_column(ForeignKey("masters.id"), nullable=False)
    datetime: Mapped[dt] = mapped_column(DateTime, nullable=False)
    name: Mapped[str] = mapped_column(String(15), nullable=False)