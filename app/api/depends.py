from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.core.const import ALGORITHM, SECRET_KEY
from app.schemas.token import TokenData
from jose import JWTError, jwt
from app.core.security import oauth2_scheme
from app.database.database import engine
from app.crud.user import user_crud

async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    db_obj = await user_crud.get_by_email(db, token_data.email)

    if db_obj is None:
        raise credentials_exception
    return db_obj