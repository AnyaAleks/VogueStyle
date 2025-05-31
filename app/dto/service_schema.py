from typing import Optional
from pydantic import Field, BaseModel, constr

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
    master_id: int
    description: Optional[str]
    price: int
    time_minutes: int

    model_config = {
        "from_attributes": True
    }