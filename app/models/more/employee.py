from sqlalchemy import Column, Integer, String, DateTime
from app.models import Base

class Employee(Base):

    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    post = Column(String(225), nullable=False)
    telephone_number = Column(String(225), nullable=False)
    birthday = Column(DateTime(True), nullable=False)

