from typing import Optional
from datetime import datetime
from pydantic import BaseModel

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
    master_id: int
    service_id: int
    user_id: int
    schedule_at: datetime

    model_config = {
        "from_attributes": True
    }