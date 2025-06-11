from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base_model import Base

if TYPE_CHECKING:
    from .master_model import MasterModel

class CertificateModel(Base):
    __tablename__ = "certificates"

    name: Mapped[str] = mapped_column(nullable=False)

    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    master: Mapped["MasterModel"] = relationship("MasterModel", back_populates="certificates")
