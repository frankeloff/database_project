from sqlalchemy import Column, Integer, String, DateTime
import datetime
from . import Base

class Visitor(Base):

    __tablename__ = "visitors"
    visitor_id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime(True), default=datetime.datetime.now)