from typing import Optional
from sqlmodel import SQLModel, Field, Column, VARCHAR


class UserBase(SQLModel):
    spotify_id: str = Field(sa_column=Column(
        "spotify_id", VARCHAR, unique=True))


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    pass
    # TODO
