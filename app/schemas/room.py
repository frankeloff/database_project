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

class SimpleRoomDataOut(BaseRoom):
    class Config:
        orm_mode = True

class RoomDataIn(BaseRoom, BaseRoomChar):
    class Config:
        orm_mode = True

class RoomDataOut(BaseRoom):
    photo: str = None
    class Config:
        orm_mode = True

class AllRoomDataOut(RoomDataOut, BaseRoomChar):
    class Config:
        orm_mode = True



