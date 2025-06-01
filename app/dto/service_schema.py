from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from pydantic import Field, BaseModel, constr

class MasterServiceGet(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    
    model_config = {
        "from_attributes": True
    }

class ServiceCreate(BaseModel):
    name: constr(max_length=64)
    master_id: int
    description: Optional[constr(max_length=256)] = None
    price: int = Field(..., ge=0)
    time_minutes: int = Field(..., ge=0)

class ServiceUpdate(BaseModel):
    name: Optional[constr(max_length=64)] = None
    description: Optional[constr(max_length=256)] = None
    price: Optional[int] = Field(None, ge=0)
    time_minutes: Optional[int] = Field(None, ge=0)

class ServiceGet(BaseModel):
    id: int
    name: str
    master: MasterServiceGet
    description: Optional[str]
    price: int
    time_minutes: int

    model_config = {
        "from_attributes": True
    }
    
ServiceGet.model_rebuild()