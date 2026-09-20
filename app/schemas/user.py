from pydantic import BaseModel, ConfigDict

ROLES = ["admin", "cashier"]

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class UserUpdate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


def sample_user() -> dict:
    return {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "role": "cashier",
        "is_active": True,
        "password": "TestPassword123!",
    }


def sample_admin() -> dict:
    return {
        "username": "testadmin",
        "first_name": "Test",
        "last_name": "Admin",
        "role": "admin",
        "is_active": True,
        "password": "AdminPassword123!",
    }