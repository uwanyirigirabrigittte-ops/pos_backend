from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class UserUpdate(UserBase):
    password: str
