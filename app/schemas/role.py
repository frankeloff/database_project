from pydantic import BaseModel

class BaseRole(BaseModel):
    role_name: str

class RoleOut(BaseRole):

    class Config:
        orm_mode = True