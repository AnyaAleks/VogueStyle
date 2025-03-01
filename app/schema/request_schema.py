from pydantic import Field, field_validator
from datetime import datetime as dt
from dateutil import parser
from .base_schema import Base

class RequestSchemaCreate(Base):
    master: int = Field(lt=10)
    datetime: dt
    name: str = Field(max_length=15)
    phone: str = Field(max_length=11)
    
    @field_validator("datetime", mode="before")
    def ensure_datatime(cls, value):
        print("Tut")
        try:
            value = parser.parse(value)
            if isinstance(value, dt):
                print("Tam")
                return f"{value.date()} {value.time()}"
        except:
            return value
        
        