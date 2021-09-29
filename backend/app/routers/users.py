from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from db.models import User, UserCreate, UserRead, UserUpdate
from db.database import get_session

router = APIRouter(
    tags=["users"],
)


# @router.post("/users/", response_model=UserRead)
# async def create_user(*, user: UserCreate, session: AsyncSession = Depends(get_session)):
#     db_user = User.from_orm(user)
#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)
#     return db_user

@router.post("/users/", response_model=User)
async def create_user(*, user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = User.from_orm(user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[User])
async def read_users(*, session: AsyncSession = Depends(get_session)):
    users = await session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users in database")
    return users


@router.get("/users/{spotify_id}", response_model=User)
async def read_user(*, session: AsyncSession = Depends(get_session), spotify_id: str):
    user = await session.exec(select(User).where(User.spotify_id == spotify_id))
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user.one()


# @router.patch("/users/{spotify_id}", response_model=User)
# async def update_user(*, session: AsyncSession = Depends(get_session), spotify_id: str, user: UserUpdate):
#     db_user = await session.get(User, spotify_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user_data = user.dict(exclude_unset=True)
#     for key, value in user_data.items():
#         setattr(db_user, key, value)
#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)
#     return db_user


@router.delete("/users/{spotify_id}", response_model=User)
async def delete_user(*, session: AsyncSession = Depends(get_session), spotify_id: str):
    user = await session.exec(select(User).where(User.spotify_id == spotify_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user.one())
    await session.commit()
    return {"deleted": user.one()}
