from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from cache import cache
from helpers.tekore_setup import spotify, auth
from helpers.spotify import get_spotify_id

from routers.users import create_user
from db.models import UserCreate
from db.database import get_session

router = APIRouter(
    tags=["auth"],
)


@router.get("/is_logged_in")
def is_logged_in(request: Request):
    user = request.session.get('user', None)
    token = cache.users.get(user, None)

    if user is None or token is None:
        request.session.pop('user', None)
        return {"isLoggedIn": False, "message": "Not logged in"}
    else:
        return {"isLoggedIn": True}


@router.get("/login")
def login(request: Request):
    if 'user' in request.session:
        return RedirectResponse(url='/overview')

    cache.auths[auth.state] = auth

    return {"url": auth.url}


@router.get("/callback")
def login_callback(request: Request, code: str, state: str):

    auth = cache.auths.pop(state, None)
    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)

    request.session['user'] = state
    cache.users[state] = token

    with spotify.token_as(token):
        new_user = UserCreate(spotify_id=get_spotify_id(spotify))
        print(new_user.spotify_id)
        # create_user(new_user)

    return RedirectResponse('http://localhost:3000/')


@router.get("/logout")
def logout(request: Request):
    uid = request.session.pop('user', None)
    if uid is not None:
        cache.users.pop(uid, None)
    return RedirectResponse('/login')
