from pydantic import BaseModel
from pydantic import EmailStr

class BaseUser(BaseModel):
    full_name: str
    telephone_number: int
    email: EmailStr

class UserIn(BaseUser):
    passport_series: int
    passport_number: int
    password: str

    class Config:
        orm_mode = True

class UserOut(BaseUser):
    
    class Config:
        orm_mode = True