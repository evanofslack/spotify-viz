from typing import Optional, List
from sqlmodel import SQLModel, Relationship, Field, Column, VARCHAR


class UserBase(SQLModel):
    spotify_id: str = Field(sa_column=Column(
        "spotify_id", VARCHAR, unique=True))
    # created_playlists: bool = False


class User(UserBase, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    playlists: Optional[List["Playlist"]] = Relationship(back_populates="user")


class UserCreate(User):
    pass


class UserRead(UserBase):
    id: int
    playlists: Optional[List["Playlist"]]


class UserUpdate(SQLModel):
    pass


class PlaylistBase(SQLModel):
    playlist_id: str
    playlist_name: str
    playlist_cover_image: str


class Playlist(PlaylistBase, table=True):
    __tablename__ = "playlist"
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="playlists")

    songs: Optional[List["Song"]] = Relationship(back_populates="playlist")


class PlaylistCreate(Playlist):
    pass


class PlaylistRead(PlaylistBase):
    id: int
    user_id: str
    user: User
    songs: Optional[List["Song"]]


class SongBase(SQLModel):
    song_id: str
    song_name: str
    artist: str


class Song(SongBase, table=True):
    __tablename__ = "song"
    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id: Optional[str] = Field(foreign_key="playlist.id")
    playlist: Optional[Playlist] = Relationship(back_populates="songs")


class SongCreate(Song):
    pass


class SongRead(SongBase):
    id: int
    playlist_id: Optional[str]
    playlist: Optional[Playlist]
