from typing import Optional, List
from pydantic import BaseModel, constr

class LocationCreate(BaseModel):
    name: constr(max_length=100)
    address: constr(max_length=200)

class LocationUpdate(BaseModel):
    name: Optional[constr(max_length=100)] = None
    address: Optional[constr(max_length=200)] = None

class LocationGet(BaseModel):
    id: int
    name: str
    address: str
    masters: List[int] = []  # list of MasterModel IDs

    model_config = {
        "from_attributes": True
    }