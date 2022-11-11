from app.models import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
import datetime

class CheckIn(Base):
    
    __tablename__ = 'checkin'
    checkin_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("room.room_id"))
    checkin_date = Column(DateTime(True), default=datetime.datetime.now)
    number_of_paid_days = Column(Integer, nullable=False)