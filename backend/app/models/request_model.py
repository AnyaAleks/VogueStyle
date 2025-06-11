from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base_model import Base

if TYPE_CHECKING:
    from .master_model import MasterModel
    from .service_model import ServiceModel
    from .user_model import UserModel

class RequestModel(Base):
    __tablename__ = "requests"

    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"), nullable=False)
    master: Mapped["MasterModel"] = relationship("MasterModel", back_populates="requests")

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    service: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="requests")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="requests")

    schedule_at: Mapped[datetime] = mapped_column(nullable=False)
