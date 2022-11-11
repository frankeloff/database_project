from app.models import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
import datetime

class Booking(Base):

    __tablename__ = 'booking'
    booking_id = Column(Integer, primary_key=True)
    visitor_id = Column(Integer, ForeignKey('visitors.visitor_id'))
    room_id =  Column(Integer, ForeignKey('room.room_id'))
    date_of_entry = Column(DateTime(True), nullable=False, default=datetime.datetime.now)
    departure_date = Column(DateTime(True), nullable=False)
    number_of_people = Column(Integer, nullable=False)