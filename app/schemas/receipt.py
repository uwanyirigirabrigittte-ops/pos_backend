from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReceiptBase(BaseModel):
    receipt_no: str
    sale_id: int
    issue_date: datetime

class ReceiptCreate(ReceiptBase):
    pass

class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class ReceiptUpdate(ReceiptBase):
    pass
