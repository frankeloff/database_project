from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)

# from .employee import Employee
# from .booking import Booking
# from .check_in import CheckIn
# from .job import Job
# from .residents import Residents
# from .room_type import Room, RoomType
from .user import User
from .role import Role, UserRole
from .visitor import Visitor
# from .services import Services, CheckinServices

__all__ = ["metadata", 'User', 'Role', 'UserRole', 'Visitor']