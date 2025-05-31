from typing import Optional, List
from datetime import date
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

class UserGet(BaseModel):
    id: int
    name: str
    surname: Optional[str]
    patronymic: Optional[str]
    birthday: Optional[date]
    tg_id: Optional[int]
    phone: str
    requests: List[int] = []

    model_config = {
        "from_attributes": True
    }
        
class UserLink(BaseModel):
    phone: str
    tg_id: int