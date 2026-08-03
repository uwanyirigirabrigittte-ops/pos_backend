from pydantic import BaseModel, ConfigDict
from typing import Optional

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    loyalty_points: int = 0

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class CustomerUpdate(CustomerBase):
    pass
