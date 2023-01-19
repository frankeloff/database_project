from sqlalchemy import Column, Integer, String, DateTime
import datetime
from . import Base


class User(Base):

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password = Column(String(60))
    passport_series = Column(String(4))
    passport_number = Column(String(6))
    telephone_number = Column(String(12))
    email = Column(String(255), unique=True)
    created_at = Column(DateTime(True), default=datetime.datetime.now)
    updated_at = Column(DateTime(True), default=datetime.datetime.now)
