from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserIn, UserOut
from app.api.depends import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud
from app.schemas.role import RoleOut

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(c: UserIn, session=Depends(get_session)):
    db_obj = await user_crud.get_by_email(session, c.email)
    if db_obj is not None:
        raise HTTPException(status_code=403, detail="User already exist")

    return await user_crud.create_user(session, c)


@router.patch("/", response_model=UserOut)
async def update_user(
    c: UserIn, session: AsyncSession = Depends(get_session), user = Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.update_user(session, db_obj, c)


@router.delete("/")
async def delete_user(session=Depends(get_session), user = Depends(get_current_user), ):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete_user(session, db_obj)

@router.get("/", response_model=RoleOut)
async def get_user_role(session=Depends(get_session), user = Depends(get_current_user)):
    return await user_crud.get_user_role(session, user.email)    