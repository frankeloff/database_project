from app.crud.base import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserIn
from app.schemas.room import AllRoomDataOut
from app.core.security import get_password_hash
from app.models import User, Room, RoomCharacteristics, UserRole, Role, Booking
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from app.core.security import verify_password
from app.schemas.room import RoomDataIn
from datetime import date
import datetime


class UserCRUD(BaseCRUD):
    async def create_user(self, db: AsyncSession, u: UserIn):
        password = u.password
        hash_password = get_password_hash(password)
        u.password = hash_password

        db_obj = User(**u.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        role_obj = UserRole(**{"user_id": db_obj.user_id, "role_id": 1})
        db.add(role_obj)
        await db.commit()
        await db.refresh(role_obj)

        return db_obj

    async def update_user(self, db: AsyncSession, db_obj: User, update_obj: UserIn):
        encoded_object_in = jsonable_encoder(db_obj)
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()

        update_data["updated_at"] = datetime.datetime.now()

        for field in encoded_object_in:
            if field in update_data:
                if field == "password":
                    setattr(db_obj, field, get_password_hash(update_data[field]))
                else:
                    setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def delete_user(self, db: AsyncSession, db_obj: User):

        query = (
            select(UserRole)
            .select_from(UserRole)
            .join(User, User.user_id == UserRole.user_id)
            .where(User.email == db_obj.email)
        )

        result = await db.execute(query)

        db_role_user_obj = result.scalars().first()

        await db.delete(db_role_user_obj)
        await db.commit()

        await db.delete(db_obj)
        await db.commit()

        return 0

    async def get_by_id(self, db: AsyncSession, client_id: int):
        query = select(User).where(User.client_id == client_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str):
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def authenticate_user(self, db: AsyncSession, email: str, password: str):
        db_obj = await self.get_by_email(db, email)
        if not verify_password(password, db_obj.password):
            return False
        return db_obj

    async def get_user_role(self, db: AsyncSession, email: str):
        query = (
            select(User.full_name, Role.role_name)
            .select_from(UserRole)
            .join(User, User.user_id == UserRole.user_id)
            .join(Role, Role.role_id == UserRole.role_id)
            .where(User.email == email)
        )

        result = await db.execute(query)

        return result.first()

    async def create_room(self, db: AsyncSession, room_data: RoomDataIn):
        room_db_obj = Room(
            **{"room_name": room_data.room_name, "is_booked": room_data.is_booked}
        )
        db.add(room_db_obj)
        await db.commit()
        await db.refresh(room_db_obj)

        room_ch_db_obj = RoomCharacteristics(
            **{
                "room_id": room_db_obj.room_id,
                "number_of_rooms": room_data.number_of_rooms,
                "floor": room_data.floor,
                "square_meters": room_data.square_meters,
                "price": room_data.price,
                "photo": room_data.photo,
            }
        )
        db.add(room_ch_db_obj)
        await db.commit()
        await db.refresh(room_ch_db_obj)

        return room_db_obj

    async def get_by_room_id(self, db: AsyncSession, room_id: int):
        query = select(Room).where(Room.room_id == room_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_room_ch_id(self, db: AsyncSession, room_id: int):
        query = select(RoomCharacteristics).where(
            RoomCharacteristics.room_id == room_id
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def update_room(self, db: AsyncSession, db_obj: Room, update_obj: RoomDataIn):
        room_ch_obj = await user_crud.get_by_room_ch_id(db, db_obj.room_id)
        encoded_object_in = jsonable_encoder(db_obj)
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()

        for field in encoded_object_in:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        encoded_object_room_ch_in = jsonable_encoder(room_ch_obj)

        for field in encoded_object_room_ch_in:
            if field in update_data:
                setattr(room_ch_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        db.add(room_ch_obj)
        await db.commit()
        await db.refresh(room_ch_obj)

        return db_obj

    async def delete_room(self, db: AsyncSession, db_obj: Room, room_id: int):
        db_room_ch_obj = await user_crud.get_by_room_ch_id(db, room_id)

        await db.delete(db_room_ch_obj)
        await db.commit()

        await db.delete(db_obj)
        await db.commit()

        return 0

    async def get_current_room(self, db: AsyncSession, db_obj: Room):
        db_room_ch_obj = await user_crud.get_by_room_ch_id(db, db_obj.room_id)
        result = AllRoomDataOut(
            room_name=db_obj.room_name,
            is_booked=db_obj.is_booked,
            number_of_rooms=db_room_ch_obj.number_of_rooms,
            floor=db_room_ch_obj.floor,
            square_meters=db_room_ch_obj.square_meters,
            price=db_room_ch_obj.price,
            photo=db_room_ch_obj.photo,
        )

        return result

    async def get_all_rooms(self, db: AsyncSession, limit: int = 200, skip: int = 0):
        query = (
            select(Room, RoomCharacteristics)
            .select_from(Room)
            .join(RoomCharacteristics, Room.room_id == RoomCharacteristics.room_id)
            .where(Room.is_booked == False)
            .limit(limit)
            .offset(skip)
        )

        result_arr = []

        result = await db.execute(query)

        for item in result.fetchall():
            res_item = AllRoomDataOut(
                room_name=item[0].room_name,
                is_booked=item[0].is_booked,
                number_of_rooms=item[1].number_of_rooms,
                floor=item[1].floor,
                square_meters=item[1].square_meters,
                price=item[1].price,
                photo=item[1].photo,
            )

            result_arr.append(res_item)

        return result_arr

    async def book_a_room(self, db: AsyncSession, mail: str, room_id: int, arrival_date, departure_date):
        db_obj = Booking(
            email=mail,
            room_id=room_id,
            arrival_date=arrival_date,
            departure_date=departure_date,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        db_room_obj = await user_crud.get_by_room_id(db, room_id)
        db_room_obj.is_booked = True
        db.add(db_room_obj)
        await db.commit()
        await db.refresh(db_room_obj)

        return 0


user_crud = UserCRUD()
