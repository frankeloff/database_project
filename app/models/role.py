from sqlalchemy import Column, Integer, String, ForeignKey
from app.models import Base


class Role(Base):
    __tablename__ = "role"
    role_id = Column(Integer, primary_key=True, nullable=False)
    role_name = Column(String(254), nullable=False)


class UserRole(Base):
    __tablename__ = "user_role"
    user_id = Column(
        Integer, ForeignKey("users.user_id"), nullable=False, primary_key=True
    )
    role_id = Column(
        Integer, ForeignKey("role.role_id"), nullable=False, primary_key=True
    )