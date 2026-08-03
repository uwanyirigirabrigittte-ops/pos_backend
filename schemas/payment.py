from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PaymentBase(BaseModel):
    sale_id: int
    method: str
    amount_paid: Decimal

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class PaymentUpdate(PaymentBase):
    pass
