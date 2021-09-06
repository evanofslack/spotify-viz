from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Dict

from db.database import Session, engine


from db.models import User, UserRead, UserCreate, UserUpdate
from db.database import get_session


def create_user(user: UserCreate):
    db_user = User.from_orm(user)
    with Session(engine) as session:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users in database")
        return users


def read_user(spotify_id: str) -> UserRead:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.spotify_id == spotify_id))
        return user.first()


def update_user(spotify_id: str, user: UserUpdate) -> UserRead:
    with Session(engine) as session:
        db_user = session.get(User, spotify_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def delete_user(spotify_id: str) -> Dict[str, UserRead]:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.spotify_id == spotify_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user.first())
        session.commit()
        return {"deleted": user.first()}
