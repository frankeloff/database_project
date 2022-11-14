from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.models import Base

class Booking(Base):
    __tablename__ = "booking"
    email =  Column(String(255), ForeignKey('users.email'), primary_key=True)
    room_id = Column(Integer, ForeignKey('room.room_id'), primary_key=True)
    arrival_date = Column(DateTime(True))
    departure_date = Column(DateTime(True))