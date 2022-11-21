from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserIn, UserOut
from app.api.depends import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud
from app.schemas.role import RoleOut
from datetime import date
from app.schemas.room import AllRoomDataOut
from typing import List
from app.schemas.order import AllBaseOrderInfo
router = APIRouter()

@router.get("/me", response_model=UserIn)
async def get_me(session=Depends(get_session), user=Depends(get_current_user),):
    return await user_crud.get_me(session, user)

@router.post("/", response_model=UserOut)
async def create_user(c: UserIn, session=Depends(get_session)):
    db_obj = await user_crud.get_by_email(session, c.email)
    if db_obj is not None:
        raise HTTPException(status_code=403, detail="User already exist")

    return await user_crud.create_user(session, c)


@router.patch("/", response_model=UserOut)
async def update_user(
    c: UserIn,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.update_user(session, db_obj, c)


@router.delete("/")
async def delete_user(
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete_user(session, db_obj)


@router.get("/", response_model=RoleOut)
async def get_user_role(session=Depends(get_session), user=Depends(get_current_user)):
    return await user_crud.get_user_role(session, user.email)

@router.get("/get_current_room/{room_id}", response_model=AllRoomDataOut)
async def get_current_room(
    room_id: int,
    session=Depends(get_session),
):
    db_room_obj = await user_crud.get_by_room_id(session, room_id)
    if not db_room_obj:
        raise HTTPException(status_code=404, detail="Room not found")

    return await user_crud.get_current_room(session, db_room_obj)

@router.get("/get_all_rooms", response_model=List[AllRoomDataOut])
async def get_all_rooms(
    skip: int = 0,
    limit: int = 200,
    session=Depends(get_session),
):

    return await user_crud.get_all_rooms(session, limit, skip)

@router.post("/booking")
async def book_a_room(
    room_id: int,
    arrival_date: str = date.today().isoformat(),
    departure_date: str = date.today().isoformat(),
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    arrival_date = date.fromisoformat(arrival_date)
    departure_date = date.fromisoformat(departure_date)
    if arrival_date > departure_date or arrival_date < date.today():
        raise HTTPException(status=400, detail="Incorrect date entry")
    return await user_crud.book_a_room(
        session, user.email, room_id, arrival_date, departure_date
    )

@router.get("/get_user_orders", response_model=List[AllBaseOrderInfo])
async def get_user_orders(
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    return await user_crud.get_user_orders(session, user.email)