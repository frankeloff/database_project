from app.crud.base import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorIn
from sqlalchemy import select
from app.models import Visitor

class VisitorCRUD(BaseCRUD):
    
    async def create_user(self, db: AsyncSession, c: VisitorIn):

        db_obj = Visitor(**c.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        return db_obj

    async def get_by_email(self, db: AsyncSession, email: str):
        query = select(Visitor).where(Visitor.email == email)
        result = await db.execute(query)
        return result.scalars().first()

visitor_crud = VisitorCRUD()