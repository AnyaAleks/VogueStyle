from datetime import time as Time
from typing import Optional
from pydantic import BaseModel, Field, conint

# === DTO ===

class MasterScheduleCreate(BaseModel):
    master_id: int
    weekday: conint(ge=0, le=6)
    start_time: Time
    end_time: Time

class MasterScheduleUpdate(BaseModel):
    weekday: Optional[conint(ge=0, le=6)] = None
    start_time: Optional[Time] = None
    end_time: Optional[Time] = None

class MasterScheduleGet(BaseModel):
    id: int
    master_id: int
    weekday: int
    start_time: Time
    end_time: Time

    model_config = {"from_attributes": True}