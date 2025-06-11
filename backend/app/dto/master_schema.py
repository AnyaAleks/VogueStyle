from __future__ import annotations
from typing import List, Optional, Union, Dict
from datetime import datetime
from fastapi import Form    
from pydantic import Field, EmailStr, constr, field_validator, BaseModel

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
    
    @classmethod
    def as_form(
        cls,
        id: int = Form(...),
        name: Optional[str] = Form(None),
        surname: Optional[str] = Form(None),
        patronymic: Optional[str] = Form(None),
        job: Optional[str] = Form(None),
        location_id: Optional[int] = Form(None),
        specialization: Optional[str] = Form(None),
        experience: Optional[int] = Form(None),
        education: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        email: Optional[EmailStr] = Form(None)
    ) -> "MasterUpdate":
        return cls(
            id=id,
            name=name,
            surname=surname,
            patronymic=patronymic,
            job=job,
            location_id=location_id,
            specialization=specialization,
            experience=experience,
            education=education,
            phone=phone,
            email=email
        )

class MasterCheck(BaseModel):
    # Use either phone or email to authenticate
    phoneemail: Union[constr(max_length=11), EmailStr]
    password: str

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
    tg_id: Optional[int]
    phone: str

    model_config = {
        "from_attributes": True
    }

class RequestMasterGet(BaseModel):
    id: int
    service: ServiceRequestGet
    user: UserRequestGet
    schedule_at: datetime

    model_config = {
        "from_attributes": True
    }
    
class ServiceMasterGet(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    time_minutes: int

    model_config = {
        "from_attributes": True
    }
    
class CertificateMasterGet(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

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
    certificates: List[CertificateMasterGet] = []
    services: List[ServiceMasterGet] = []
    requests: List[RequestMasterGet] = []

    model_config = {
        "from_attributes": True
    }

class MasterPasswordUpdate(BaseModel):
    phone: str = Field(max_length=11)
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
    
MasterGet.model_rebuild()