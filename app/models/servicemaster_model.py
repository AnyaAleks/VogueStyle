from sqlalchemy import Table, Column, Integer, ForeignKey
from .base_model import Base

services_masters = Table(
    "services_masters",
    Base.metadata,
    Column("master_id", Integer, ForeignKey("masters.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
)