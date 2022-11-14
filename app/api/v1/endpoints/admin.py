from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserIn, UserOut
from app.api.depends import get_session, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud
from app.crud.user import user_crud
from app.schemas.room import RoomDataIn, RoomDataOut
from fastapi import UploadFile, File
from aiofile import async_open
import os

router = APIRouter()


@router.patch("/", response_model=UserOut)
async def update_user(
    email: str,
    c: UserIn,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    role = await user_crud.get_user_role(session, user.email)
    if role[0] != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await user_crud.update_user(session, db_obj, c)


@router.delete("/")
async def delete_user(
    email: str,
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    role = await user_crud.get_user_role(session, user.email)
    if role[1] != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await user_crud.delete_user(session, db_obj)

@router.post("/create_room", response_model=RoomDataOut)
async def create_room(
    r: RoomDataIn,
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    role = await user_crud.get_user_role(session, user.email)
    if role[1] != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await user_crud.create_room(session, r)

@router.patch("/update_room", response_model=RoomDataOut)
async def update_room(
    room_id: int,
    r: RoomDataIn,
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    role = await user_crud.get_user_role(session, user.email)
    if role[1] != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")
    db_room_obj = await user_crud.get_by_room_id(session, room_id)
    if not db_room_obj:
        raise HTTPException(status_code=404, detail="Room not found")

    return await user_crud.update_room(session, db_obj, r)

@router.delete("/delete_room", response_model=bool)
async def delete_room(
    room_id: int,
    session=Depends(get_session),
    user=Depends(get_current_user),
):
    db_obj = await user_crud.get_by_email(session, user.email)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
    role = await user_crud.get_user_role(session, user.email)
    if role[1] != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")
    db_room_obj = await user_crud.get_by_room_id(session, room_id)
    if not db_room_obj:
        raise HTTPException(status_code=404, detail="Room not found")

    return await user_crud.delete_room(session, db_room_obj, room_id)



# @router.post("/uploadfile/")
# async def create_upload_file(
#     file: UploadFile = File(description="A file read as UploadFile"),
# ):
#     syf = file.filename.split('.')[1]
#     async with async_open(f'out_file.{syf}', 'wb') as f:
#         try:
#             while chunk:= await file.read(1024):
#                 await f.write(chunk)
#                 print('asdfsadf')
#         except:
#             raise HTTPException(status_code=404, detail='File not found')
#     print(os.path.abspath(f'out_file.{syf}'))
#     return "okey"