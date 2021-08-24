import uvicorn
import tekore as tk
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from typing import List

# from app.config import get_settings, Settings #___DOCKER___ "proxy": "http://host.docker.internal:8080",
from config import get_settings, Settings
from helpers.spotify import get_display_name, get_currently_playing, get_last_played

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="yeahyouthought")

origins = [
    'http://localhost',
    'localhost'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# file = './app/tekore.cfg' #___DOCKER___
file = 'tekore.cfg'
conf = tk.config_from_file(file)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)


@app.get("/ping")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }


@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, spotify_id=user.spotify_id)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Spotify ID already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db)
    return users


@app.get("/is_logged_in")
def is_logged_in(request: Request):
    user = request.session.get('user', None)
    token = users.get(user, None)
    '''
    token = get_token_from_db(state: Str)
    '''

    if user is None or token is None:
        request.session.pop('user', None)
        return {"isLoggedIn": False, "message": "Not logged in"}
    else:
        return {"isLoggedIn": True}


@app.get("/overview")
def read_root(request: Request):
    user = request.session.get('user', None)
    token = users.get(user, None)

    if user is None or token is None:
        request.session.pop('user', None)
        return RedirectResponse(url='/login')

    if token.is_expiring:
        token = cred.refresh(token)
        users[user] = token

    try:
        with spotify.token_as(token):

            display_name = get_display_name(spotify)

            current = get_currently_playing(spotify)

            last = get_last_played(spotify)

    except tk.HTTPError as err:
        print(str(err))
        # print(err.response)
        # print(err.request)
        return {"error": "Could not fetch info"}
    return {"display_name": display_name,
            "current_song": current['current_song'],
            "current_artist": current['current_artist'],
            "last_song": last['last_song'],
            "last_artist": last['last_artist'],
            "elapsed_time": last['elapsed_time'],
            "time_units": last['time_units'],
            }


@ app.get("/login")
def login(request: Request):
    if 'user' in request.session:
        return RedirectResponse(url='/home')

    scope = tk.scope.user_read_currently_playing + \
        tk.scope.user_read_playback_state + tk.scope.user_read_recently_played
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    '''
    update_user_db(auth.state, auth)
    '''
    return {"url": auth.url}


@ app.get("/callback")
def login_callback(request: Request, code: str, state: str):

    auth = auths.pop(state, None)

    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)

    request.session['user'] = state
    users[state] = token
    return RedirectResponse('http://localhost:3000/')


@ app.get("/logout")
def logout(request: Request):
    uid = request.session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return RedirectResponse('/login')


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8080, host='0.0.0.0', reload=True,
    )
