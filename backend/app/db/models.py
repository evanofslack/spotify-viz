from typing import Optional, List
from sqlmodel import SQLModel, Relationship, Field, Column, VARCHAR


class UserBase(SQLModel):
    spotify_id: str = Field(sa_column=Column(
        "spotify_id", VARCHAR, unique=True))


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


class Playlist(PlaylistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="playlists")


class PlaylistCreate(Playlist):
    pass


class PlaylistRead(PlaylistBase):
    id: int
    user_id: str
    user: User
