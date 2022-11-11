from pydantic import BaseModel

class BaseRole(BaseModel):
    full_name: str
    role_name: str

class RoleOut(BaseRole):

    class Config:
        orm_mode = True