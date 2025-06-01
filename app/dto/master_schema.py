from __future__ import annotations
from typing import List, Optional, Union, Dict
from datetime import time as Time
from pydantic import Field, EmailStr, constr, field_validator, BaseModel
from .certificate_schema import CertificateGet
from .service_schema import ServiceGet

class MasterCreate(BaseModel):
    name: constr(max_length=30)
    surname: constr(max_length=30)
    patronymic: Optional[constr(max_length=30)] = None
    job: Optional[str] = None
    location_id: int
    specialization: Optional[str] = None
    experience: Optional[int] = Field(None, gt=0, lt=100)
    education: Optional[str] = None
    phone: constr(max_length=11)
    email: Optional[EmailStr] = None
    password: constr(min_length=6)
    photo_link: Optional[str] = None
    
    @field_validator("phone", mode='before')
    @classmethod
    def phone_validator(cls, value: str):
        if len(value) == 12:
            return "8"+value[2:]
        return value

class MasterUpdate(BaseModel):
    id: int
    name: Optional[constr(max_length=30)] = None
    surname: Optional[constr(max_length=30)] = None
    patronymic: Optional[constr(max_length=30)] = None
    job: Optional[str] = None
    location_id: Optional[int] = None
    specialization: Optional[str] = None
    experience: Optional[int] = Field(None, gt=0, lt=100)
    education: Optional[str] = None
    phone: Optional[constr(max_length=11)] = None
    email: Optional[EmailStr] = None
    photo_link: Optional[str] = None
    
    @field_validator("phone", mode='before')
    @classmethod
    def phone_validator(cls, value: str):
        if len(value) == 12:
            return "8"+value[2:]
        return value

class MasterCheck(BaseModel):
    # Use either phone or email to authenticate
    phoneemail: Union[constr(max_length=11), EmailStr]
    password: str

class MasterGet(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: Optional[str]
    job: Optional[str]
    location_id: int
    specialization: Optional[str]
    experience: Optional[int]
    education: Optional[str]
    phone: str
    email: Optional[EmailStr]
    photo_link: Optional[str]
    available_slots: Dict = []
    certificates: List[CertificateGet] = []
    services: List[ServiceGet] = []

    model_config = {
        "from_attributes": True
    }

class MasterPasswordUpdate(BaseModel):
    phone: str = Field(max_length=11)
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)