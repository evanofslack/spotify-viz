from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from typing import Dict, List

from db.database import async_session
from db.models import (User,
                       UserRead,
                       UserCreate,
                       UserUpdate,
                       Playlist,
                       PlaylistCreate,
                       PlaylistRead,
                       Song,
                       SongCreate,
                       SongRead)

""" Crud database functions """


async def create_user(user: UserCreate) -> UserRead:
    """
    Create user

    """
    db_user = User.from_orm(user)
    async with async_session() as session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


async def read_users() -> List[UserRead]:
    """
    Read all users 

    """
    async with async_session() as session:
        users = await session.execute(select(User)).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users in database")
        return users


async def read_user(spotify_id: str) -> UserRead:
    """
    Create user from spotify ID

    """
    async with async_session() as session:
        try:
            query = await session.execute(select(User).where(User.spotify_id == spotify_id))
            # List comp on a returned tuple
            users = [user for user in query.one()]
            return users[0]
        except NoResultFound:
            # raise HTTPException(status_code=404, detail="User not found")
            return None

        except MultipleResultsFound:
            raise HTTPException(status_code=404, detail="Multiple users found")


async def update_user(user_id: str, user: UserUpdate) -> UserRead:
    """
    Update a user's attributes

    """
    async with async_session() as session:
        db_user = await session.get(User, user_id)
        # query = await session.execute(select(User).where(User.spotify_id == spotify_id))
        # users = [user for user in query.one()]
        # db_user = users[0]
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
    """
    Delete user

    """
    async with async_session() as session:
        user = await session.execute(select(User).where(User.spotify_id == spotify_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user.first())
        await session.commit()
        return {"deleted": user.first()}


async def create_playlist(playlist: PlaylistCreate) -> Playlist:
    """
    Create playlist

    """
    db_playlist = Playlist.from_orm(playlist)
    async with async_session() as session:
        session.add(db_playlist)
        await session.commit()
        await session.refresh(db_playlist)
        return db_playlist


async def read_playlist(playlist_id: str) -> PlaylistRead:
    """
    Read playlist by playlist ID

    """
    async with async_session() as session:
        try:
            query = await session.execute(select(Playlist).where(Playlist.playlist_id == playlist_id))
            # List comp on a returned tuple
            playlists = [playlist for playlist in query.one()]
            return playlists[0]
        except NoResultFound:
            # raise HTTPException(status_code=404, detail="Playlist not found")
            return None

        except MultipleResultsFound:
            raise HTTPException(status_code=404, detail="Multiple users found")


async def read_playlists(user_id: str) -> List[PlaylistRead]:
    """
    Read all user's playlists

    """
    async with async_session() as session:
        query = await session.execute(select(Playlist).where(Playlist.user_id == user_id))
        playlists = [playlist for playlist, in query.all()]
        if not playlists:
            raise HTTPException(
                status_code=404, detail="User has no playlists")
        return playlists


async def create_song(song: SongCreate) -> SongRead:
    """
    Create song

    """
    db_song = Song.from_orm(song)
    async with async_session() as session:
        session.add(db_song)
        await session.commit()
        await session.refresh(db_song)
        return db_song


async def read_song(song_id: str) -> SongRead:
    """
    Read song

    """
    async with async_session() as session:
        try:
            query = await session.execute(select(Song).where(Song.song_id == song_id))
            # List comp on a returned tuple
            songs = [song for song in query.one()]
            return songs[0]
        except NoResultFound:
            # raise HTTPException(status_code=404, detail="Playlist not found")
            return None

        except MultipleResultsFound:
            raise HTTPException(status_code=404, detail="Multiple songs found")


async def read_user_songs(user_id: str) -> List[SongRead]:
    """
    Read user's songs

    """
    async with async_session() as session:
        query = await session.execute(select(Song).where(Song.user_id == user_id))
        songs = [song for song, in query.all()]
        if not songs:
            raise HTTPException(
                status_code=404, detail="User has no songs")
        return songs


async def read_playlist_songs(playlist_id: str) -> List[SongRead]:
    """
    Read all songs from a playlist

    """
    async with async_session() as session:
        query = await session.execute(select(Song).where(Song.playlist_id == playlist_id))
        songs = [song for song, in query.all()]
        if not songs:
            raise HTTPException(
                status_code=404, detail="Playlist has no songs")
        return songs
