from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    spotify_id: int
    token: str
    session_id: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    pass
