from .base_model import Base
from .request_model import RequestModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import List

class MasterModel(Base):
    __tablename__ = "masters" # type: ignore
    
    requests: Mapped[List['RequestModel']] = relationship()
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)