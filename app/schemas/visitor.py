from pydantic import BaseModel
from pydantic import EmailStr


class BaseVisitor(BaseModel):
    full_name: str
    email: EmailStr


class VisitorIn(BaseVisitor):
    class Config:
        orm_mode = True


class VisitorOut(BaseVisitor):
    class Config:
        orm_mode = True
