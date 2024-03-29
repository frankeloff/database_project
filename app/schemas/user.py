from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class BaseUser(BaseModel):
    full_name: str
    telephone_number: str
    email: EmailStr


class UserIn(BaseUser):
    passport_series: str
    passport_number: str
    password: Optional[str]

    class Config:
        orm_mode = True


class UserOut(BaseUser):
    class Config:
        orm_mode = True
