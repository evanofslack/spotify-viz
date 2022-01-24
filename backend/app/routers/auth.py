import tekore as tk
from cache import cache
from db.models import Login, RedirectURL
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from helpers.spotify import get_spotify_id
from helpers.tekore_setup import cred, scope, spotify

router = APIRouter(
    tags=["auth"],
)

@router.get("/is_logged_in", response_model=Login)
async def is_logged_in(request: Request):
    """
    Index cache to determine is user is logged in

    """
    user = request.session.get('user', None)
    token = cache.users.get(user, None)

    if user is None or token is None:
        request.session.pop('user', None)
        return {"is_logged_in": False, "message": "Not logged in"}
    else:
        return {"is_logged_in": True, "message": "Sucessfully logged in"}


@router.get("/login", response_model=RedirectURL)
async def login(request: Request):
    """
    Return spotify login url 

    """
    if 'user' in request.session:
        return RedirectResponse(url='/overview')

    auth = tk.UserAuth(cred, scope)
    cache.auths[auth.state] = auth
    print("State:")
    print(auth.state)
    print("Cache:")
    print(cache.auths)
    print("Cache State:")
    print(cache.auths.pop(auth.state, None))

    return {"url": auth.url}


@router.get("/callback")
async def login_callback(request: Request, code: str, state: str) -> RedirectResponse:
    """
    Create user and return redirect url to home page

    """
    
    print("Cache After:")
    print(cache.auths)
    print("URL State")
    print(state)
    auth = cache.auths.pop(state, None)
    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)

    request.session['user'] = state
    cache.users[state] = token

    with spotify.token_as(token):
        spotify_id = await get_spotify_id(spotify)

    return RedirectResponse('http://localhost:3000/')


@ router.get("/logout")
def logout(request: Request) -> RedirectResponse:
    """
    Remove user from cache 

    """
    uid = request.session.pop('user', None)
    if uid is not None:
        cache.users.pop(uid, None)
    return RedirectResponse('/login')
