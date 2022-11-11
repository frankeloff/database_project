from ast import For
from app.models import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

class Services(Base):
    
    __tablename__ = 'services'
    name_of_the_service = Column(String(100), primary_key=True)
    price = Column(Integer, nullable=False)

class CheckinServices(Base):

    __tablename__ = 'checkin_services'
    name_of_the_service = Column(String(100), ForeignKey("services.name_of_the_service"), primary_key=True)
    checkin_id = Column(Integer, ForeignKey("checkin.checkin_id"), primary_key=True)
    quantity = Column(String, nullable=False, default=1)
