from pydantic import Field, PositiveInt
from .base_schema import Base

class MasterSchemaCreate(Base):
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    patronymic: str = Field(max_length=30, default="")
    phone: str = Field(max_length=11)
    password: str = Field()
    
class MasterSchemaGet(Base):
    id: PositiveInt
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    patronymic: str = Field(max_length=30)
    phone: str = Field(max_length=11)
    
class MasterSchemaUpdate(Base):
    id: PositiveInt
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    patronymic: str = Field(max_length=30)
    phone: str = Field(max_length=11)
    
class MasterSchemaCheck(Base):
    phone: str = Field(max_length=11)
    password: str

class MasterSchemaUpdatePassword(Base):
    phone: str = Field(max_length=11)
    old_password: str
    new_password: str