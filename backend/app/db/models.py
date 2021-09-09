from typing import Optional, List
from sqlmodel import SQLModel, Relationship, Field, Column, VARCHAR


class UserBase(SQLModel):
    spotify_id: str = Field(sa_column=Column(
        "spotify_id", VARCHAR, unique=True))


class User(UserBase, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    playlists: Optional[List["Playlist"]] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    pass


class Playlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id: str
    spotify_id: str = Field(foreign_key="user.spotify_id")
    user: User = Relationship(back_populates="playlists")


class PlaylistBase(SQLModel):
    pass


# class Playlist(PlaylistBase):
#     id: Optional[int] = Field(default=None, primary_key=True)


class PlaylistCreate(PlaylistBase):
    pass
