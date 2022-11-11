from app.crud.base import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserIn
from app.core.security import get_password_hash
from app.models.user import User
from app.models.role import UserRole, Role
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from app.core.security import verify_password
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


user_crud = UserCRUD()
