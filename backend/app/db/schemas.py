from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    spotify_id: int
    id: int
    state: str
    token: str


class UserCreate(BaseModel):
    state: str
    token: str
    spotify_id: int
