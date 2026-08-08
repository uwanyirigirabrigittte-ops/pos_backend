from pydantic import BaseModel, ConfigDict
from typing import Optional

class SupplierBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    phone: str
    email: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class SupplierUpdate(SupplierBase):
    pass
