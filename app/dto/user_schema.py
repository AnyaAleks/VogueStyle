from typing import Union
from .base_schema import Base
from pydantic import Field, PositiveInt

class UserSchemaGet(Base):
    id: PositiveInt
    name: str
    tg_id: Union[PositiveInt, None]
    phone: str = Field(max_length=11)
    
class UserSchemaCreate(Base):
    name: str
    tg_id: PositiveInt = Field(default=None)
    phone: str
    password: str
    
class UserSchemaCheck(Base):
    phone: str = Field(max_length=11)
    password: str
    
class UserSchemaLink(Base):
    id: PositiveInt
    tg_id: PositiveInt