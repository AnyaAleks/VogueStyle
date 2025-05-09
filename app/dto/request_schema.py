from datetime import datetime as dt
from pydantic import PositiveInt, field_validator
from dateutil import parser
from .base_schema import Base
from .master_schema import MasterSchemaGet
from .user_schema import UserSchemaGet
from .service_schema import ServiceSchemaGet

class RequestSchemaCreate(Base):
    master_id: PositiveInt
    service_id: PositiveInt
    user_id: PositiveInt
    datetime: dt
    
    @field_validator("datetime", mode="before")
    def ensure_datatime(cls, value):
        try:
            value = parser.parse(value)
            if isinstance(value, dt):
                return f"{value.date()} {value.time()}"
        except Exception:
            return value
        
class RequestSchemaGet(Base):
    id: PositiveInt
    master: MasterSchemaGet
    user: UserSchemaGet
    service: ServiceSchemaGet
    datetime: dt
    
    @field_validator("datetime", mode="before")
    def ensure_datatime(cls, value):
        try:
            value = parser.parse(value)
            if isinstance(value, dt):
                return f"{value.date()} {value.time()}"
        except Exception:
            return value