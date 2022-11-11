from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserIn, UserOut
from app.api.depends import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.visitor import visitor_crud
from app.schemas.visitor import VisitorOut, VisitorIn

router = APIRouter()

@router.post("/", response_model=VisitorOut)
async def create_visitor(v: VisitorIn, session=Depends(get_session)):
    db_obj = await visitor_crud.get_by_email(session, v.email)
    if db_obj is not None:
        raise HTTPException(status_code=403, detail="User already exist")

    return await visitor_crud.create_user(session, v)