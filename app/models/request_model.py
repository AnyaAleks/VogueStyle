from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime as dt

class RequestModel(Base):
    __tablename__ = "requests"
    
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    datetime: Mapped[dt] = mapped_column(DateTime, nullable=False)