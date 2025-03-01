from pydantic import Field
from .base_schema import Base

class MasterSchemaCreate(Base):
    fullname: str = Field(max_length=15)
    phone: str = Field(max_length=11)
