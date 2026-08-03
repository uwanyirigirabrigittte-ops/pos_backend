from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class CategoryUpdate(CategoryBase):
    pass
