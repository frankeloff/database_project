from app.models import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class RoomType(Base):

    __tablename__ = 'room_type'
    category = Column(String(100), nullable=True, primary_key=True)
    price = Column(Integer, default=1)
    сapacity = Column(Integer, nullable=False, default=1)
    size = Column(Integer, nullable=False, default=10)
    shower = Column(Boolean, nullable=False)
    type_of_bed = Column(String(30), nullable=False)
    conditioner = Column(Boolean, nullable=False, default=False)

class Room(Base):

    __tablename__ = 'room'
    room_id = Column(Integer, primary_key=True)
    category = Column(String(100), ForeignKey('room_type.category'))
    status = Column(String(50))
    view = Column(String(100), nullable=False)

