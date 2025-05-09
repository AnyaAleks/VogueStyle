from pydantic import Field, PositiveInt
from .base_schema import Base

class ServiceSchemaCreate(Base):
    name: str = Field(max_length=15)
    description: str = Field(max_length=40, default="")
    price: PositiveInt
    time_minutes: PositiveInt
    
class ServiceSchemaGet(Base):
    id: PositiveInt
    name: str
    description: str
    price: PositiveInt
    time_minutes: PositiveInt
    
class ServiceSchemaUpdate(Base):
    id: PositiveInt
    name: str
    description: str
    price: PositiveInt
    time_minutes: PositiveInt