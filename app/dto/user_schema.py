from typing import Optional, List
from datetime import date, datetime
from pydantic import constr, BaseModel

class UserCreate(BaseModel):
    name: constr(max_length=30)
    surname: Optional[constr(max_length=30)] = None
    patronymic: Optional[constr(max_length=30)] = None
    birthday: Optional[date] = None
    tg_id: Optional[int] = None
    phone: constr(min_length=11, max_length=12)

class UserUpdate(BaseModel):
    name: Optional[constr(max_length=30)] = None
    surname: Optional[constr(max_length=30)] = None
    patronymic: Optional[constr(max_length=30)] = None
    birthday: Optional[date] = None
    tg_id: Optional[int] = None
    phone: Optional[constr(min_length=11, max_length=12)] = None

class MasterRequestGet(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    
    model_config = {
        "from_attributes": True
    }
    
class ServiceRequestGet(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    time_minutes: int

    model_config = {
        "from_attributes": True
    }

class RequestUserGet(BaseModel):
    id: int
    master: MasterRequestGet
    service: ServiceRequestGet
    schedule_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserGet(BaseModel):
    id: int
    name: str
    surname: Optional[str]
    patronymic: Optional[str]
    birthday: Optional[date]
    tg_id: Optional[int]
    phone: str
    requests: List[RequestUserGet] = []

    model_config = {
        "from_attributes": True
    }
        
class UserLink(BaseModel):
    phone: str
    tg_id: int
    
UserGet.model_rebuild()