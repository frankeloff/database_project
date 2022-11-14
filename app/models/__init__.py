from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)

from .user import User
from .role import Role, UserRole
from .room import Room, RoomCharacteristics
from .booking import Booking

__all__ = ["metadata", 'User', 'Role', 'UserRole', 'Booking', 'Room', 'RoomCharacteristics']