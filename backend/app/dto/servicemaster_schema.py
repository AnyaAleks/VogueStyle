from pydantic import BaseModel

class ServiceMasterLink(BaseModel):
    master_id: int
    service_id: int
    
    model_config = {
        "from_attributes": True
    }