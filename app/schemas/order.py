from pydantic import BaseModel
from .room import BaseRoom, BaseRoomChar
from datetime import date

class BaseOrder(BaseModel):
    email: str
    room_id: int
    arrival_date: str = date.today().isoformat()
    departure_date: str = date.today().isoformat()

class OrderIn(BaseOrder):
    class Config:
        orm_mode = True

class OrderOut(BaseOrder):
    class Config:
        orm_mode = True


class AllBaseOrderInfo(BaseOrder, BaseRoom, BaseRoomChar):
    class Config:
        orm_mode = True

