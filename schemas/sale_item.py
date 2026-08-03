from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class SaleItemBase(BaseModel):
    sale_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal

class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class SaleItemUpdate(SaleItemBase):
    pass
