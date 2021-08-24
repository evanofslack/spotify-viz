from sqlalchemy.orm import Session
from db import models, schemas


def get_user_by_state(db: Session, state: str):
    return db.query(models.User).filter(models.User.state == state).first()


def get_user_by_id(db: Session, spotify_id: int):
    return db.query(models.User).filter(models.User.spotify_id == spotify_id).first()


def update_user(db: Session, state: str, token: str):
    pass


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(state=user.state, token=user.token,
                          spotify_id=user.spotify_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user
