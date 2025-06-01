from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel

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
    
class UserRequestGet(BaseModel):
    id: int
    name: str
    surname: Optional[str]
    patronymic: Optional[str]
    birthday: Optional[date]
    tg_id: Optional[int]
    phone: str

    model_config = {
        "from_attributes": True
    }

class RequestCreate(BaseModel):
    master_id: int
    service_id: int
    user_id: int
    schedule_at: datetime

class RequestUpdate(BaseModel):
    master_id: Optional[int] = None
    service_id: Optional[int] = None
    user_id: Optional[int] = None
    schedule_at: Optional[datetime] = None

class RequestGet(BaseModel):
    id: int
    master: MasterRequestGet
    service: ServiceRequestGet
    user: UserRequestGet
    schedule_at: datetime

    model_config = {
        "from_attributes": True
    }
    
RequestGet.model_rebuild()