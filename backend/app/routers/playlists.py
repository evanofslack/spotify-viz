from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List


from models.user import User, UserCreate, UserRead, UserUpdate
from models.playlist import Playlist, PlaylistCreate
from db.database import get_session

router = APIRouter(
    tags=["playlist"],
)


@router.post("/users/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# @router.get("/users/", response_model=List[User])
# def read_users(*, session: Session = Depends(get_session)):
#     users = session.exec(select(User)).all()
#     if not users:
#         raise HTTPException(status_code=404, detail="No users in database")
#     return users


# @router.get("/users/{spotify_id}", response_model=UserRead)
# def read_user(*, session: Session = Depends(get_session), spotify_id: str):
#     user = session.exec(select(User).where(User.spotify_id == spotify_id))
#     if not user:
#         raise HTTPException(status_code=404, detail="user not found")
#     return user.one()


# @ router.patch("/users/{spotify_id}", response_model=UserRead)
# def update_user(*, session: Session = Depends(get_session), spotify_id: str, user: UserUpdate):
#     db_user = session.get(User, spotify_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user_data = user.dict(exclude_unset=True)
#     for key, value in user_data.items():
#         setattr(db_user, key, value)
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user


# @ router.delete("/users/{spotify_id}", response_model=UserRead)
# def delete_user(*, session: Session = Depends(get_session), spotify_id: str):
#     user = session.exec(select(User).where(User.spotify_id == spotify_id))

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     session.delete(user.one())
#     session.commit()
#     return {"deleted": user.one()}
