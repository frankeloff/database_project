from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.models import Base


class Room(Base):
    __tablename__ = "room"
    room_id = Column(Integer, primary_key=True)
    room_name = Column(String(100), nullable=False)
    is_booked = Column(Boolean, nullable=False)

class RoomCharacteristics(Base):
    __tablename__ = "char_room"
    room_id = Column(Integer, ForeignKey('room.room_id'), primary_key=True)
    number_of_rooms = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    square_meters = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    photo = Column(String)
