from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, unique=True, index=True)
    token = Column(String)
    spotify_id = Column(Integer, unique=True)
