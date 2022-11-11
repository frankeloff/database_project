from app.models import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

class Residents(Base):

    __tablename__ = 'residents'
    checkin_id = Column(Integer, ForeignKey('checkin.checkin_id'), primary_key=True)
    visitor_id = Column(Integer, ForeignKey('visitors.visitor_id'), primary_key=True)

