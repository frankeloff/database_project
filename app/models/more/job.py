import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.models import Base

class Job(Base):

    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    room_id = Column(Integer, ForeignKey("room.room_id"))
    title = Column(String(100), nullable=False)
    execution_time = Column(DateTime(True), default=datetime.datetime.now)
