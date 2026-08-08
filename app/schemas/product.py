from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    barcode: str
    name: str
    cost_price: Decimal
    retail_price: Decimal
    quantity: int
    category_id: int
    supplier_id: int
    image_url: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class ProductUpdate(ProductBase):

    id: int
