import uvicorn
import tekore as tk
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from typing import List
from sqlmodel import Session, select

from db.models import User, UserCreate, UserRead, UserUpdate
from db.database import create_db_and_tables, get_session
from config import get_settings, Settings
from helpers.spotify import get_display_name, get_currently_playing, get_last_played


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


file = 'tekore.cfg'  # file = './app/tekore.cfg'
conf = tk.config_from_file(file)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

# TODO: Move session data into db
auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# TODO: Group routes into seperate router files
@app.post("/users/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[User])
def read_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users in database")
    return users


@app.get("/users/{spotify_id}", response_model=UserRead)
def read_user(*, session: Session = Depends(get_session), spotify_id: int):
    user = session.get(User, spotify_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.patch("/users/{spotify_id}", response_model=UserRead)
def update_user(*, session: Session = Depends(get_session), spotify_id: int, user: UserUpdate):
    db_user = session.get(User, spotify_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/users/{spotify_id}")
def delete_user(*, session: Session = Depends(get_session), spotify_id: int):
    user = session.get(User, spotify_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


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


@app.get("/ping")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8080, host='0.0.0.0', reload=True,
    )
