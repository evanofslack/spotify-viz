from fastapi import HTTPException
from sqlmodel import select
from typing import Dict, List

from db.database import async_session
from db.models import User, UserRead, UserCreate, UserUpdate, Playlist, PlaylistCreate, Song, SongCreate, SongRead


async def create_user(user: UserCreate) -> User:
    db_user = User.from_orm(user)
    async with async_session() as session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


async def read_users() -> List[UserRead]:
    async with async_session() as session:
        users = await session.execute(select(User)).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users in database")
        return users


async def read_user(spotify_id: str) -> UserRead:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.spotify_id == spotify_id))
        return user.first()


async def update_user(spotify_id: str, user: UserUpdate) -> UserRead:
    async with async_session() as session:
        db_user = await session.get(User, spotify_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


async def delete_user(spotify_id: str) -> Dict[str, UserRead]:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.spotify_id == spotify_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user.first())
        await session.commit()
        return {"deleted": user.first()}


async def create_playlist(playlist: PlaylistCreate) -> Playlist:
    db_playlist = Playlist.from_orm(playlist)
    async with async_session() as session:
        session.add(db_playlist)
        await session.commit()
        await session.refresh(db_playlist)
        return db_playlist


async def create_song(song: SongCreate) -> SongRead:
    db_song = Song.from_orm(song)
    async with async_session() as session:
        session.add(db_song)
        await session.commit()
        await session.refresh(db_song)
        return db_song
