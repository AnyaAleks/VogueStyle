from typing import Optional
from pydantic import BaseModel, constr

class CertificateCreate(BaseModel):
    name: constr(max_length=100)
    master_id: int

class CertificateUpdate(BaseModel):
    name: Optional[constr(max_length=100)] = None

class CertificateGet(BaseModel):
    id: int
    name: str
    master_id: int

    model_config = {
        "from_attributes": True
    }