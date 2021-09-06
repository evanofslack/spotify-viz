from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import tekore as tk

from helpers.tekore_setup import spotify, cred, scope
from helpers.spotify import get_spotify_id
from helpers.crud import create_user, read_user

from db.models import UserCreate
from cache import cache

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

    auth = tk.UserAuth(cred, scope)
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
        spotify_id = get_spotify_id(spotify)
        if read_user(spotify_id=spotify_id):
            print("User with ID: ", spotify_id, "already exists")
            # update_user
        else:
            new_user = UserCreate(spotify_id=spotify_id)
            create_user(user=new_user)
            print("Created new user with ID: ", new_user.spotify_id)

    return RedirectResponse('http://localhost:3000/')


@router.get("/logout")
def logout(request: Request):
    uid = request.session.pop('user', None)
    if uid is not None:
        cache.users.pop(uid, None)
    return RedirectResponse('/login')
