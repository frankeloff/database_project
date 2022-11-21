from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, PrimaryKeyConstraint
from app.models import Base

class Booking(Base):
    __tablename__ = "booking"
    email =  Column(String(255), ForeignKey('users.email'))
    room_id = Column(Integer, ForeignKey('room.room_id'))
    arrival_date = Column(DateTime(True))
    departure_date = Column(DateTime(True))
    __table_args__ = (PrimaryKeyConstraint("email", "room_id", name="booking_pk"),)