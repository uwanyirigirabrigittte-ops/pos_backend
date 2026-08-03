from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional
from schemas.sale_item import SaleItemCreate

class SaleBase(BaseModel):
    sale_date: datetime
    sub_total: Decimal
    tax_amount: Decimal
    discount: Decimal
    grand_total: Decimal
    user_id: int
    customer_id: Optional[int] = None

class SaleCreate(SaleBase):
    items: list[SaleItemCreate]  # To allow embedding cart items during checkout

class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class SaleUpdate(SaleBase):
    pass
