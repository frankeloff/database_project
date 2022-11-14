from typing import Union
from pydantic import BaseModel
from fastapi import UploadFile

class BaseRoom(BaseModel):
    room_name: str
    is_booked: bool

class BaseRoomChar(BaseModel):
    number_of_rooms: int
    floor: int
    square_meters: int
    price: int
    photo: str

class RoomDataIn(BaseRoom, BaseRoomChar):
    class Config:
        orm_mode = True

class RoomDataOut(BaseRoom):
    class Config:
        orm_mode = True

class AllRoomDataOut(BaseRoom, BaseRoomChar):
    class Config:
        orm_mode = True



