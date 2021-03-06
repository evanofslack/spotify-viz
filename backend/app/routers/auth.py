from config import Settings, get_settings
from connections import redis_cache
from db.models import Login, RedirectURL
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from helpers.spotify import get_spotify_id, token_to_dict
from helpers.tekore_setup import cred, scope, spotify
from tekore._auth.util import gen_state

router = APIRouter(
    tags=["auth"],
)


@router.get("/is_logged_in", response_model=Login)
async def is_logged_in(request: Request):
    """
    Index session and cache to determine is user is logged in

    """
    id = request.session.get("user", None)
    if id is None:
        print("no matching id")
        request.session.pop("user", None)
        return {"is_logged_in": False, "message": "Not logged in"}

    token_info = await redis_cache.hgetall(id)
    if token_info is None:
        print("No token info")
        request.session.pop("user", None)
        return {"is_logged_in": False, "message": "Not logged in"}
    else:
        return {"is_logged_in": True, "message": "Successfully logged in"}


@router.get("/login", response_model=RedirectURL)
async def login(request: Request):
    """
    Return spotify login url

    """
    if "user" in request.session:
        return RedirectResponse(url="/overview")

    state = gen_state()
    await redis_cache.set(state, "true")
    url = cred.user_authorisation_url(scope, state)

    return {"url": url}


@router.get("/callback")
async def login_callback(
    request: Request, code: str, state: str, settings: Settings = Depends(get_settings)
) -> RedirectResponse:
    """
    Create user and return redirect url to home page

    """
    if not await redis_cache.exists(state):
        return "Invalid state!", 400

    token = cred.request_user_token(code)
    with spotify.token_as(token):
        spotify_id = await get_spotify_id(spotify)

    request.session["user"] = spotify_id
    token_info = token_to_dict(token)
    await redis_cache.hmset(spotify_id, token_info)

    return RedirectResponse(settings.home_url)


@router.get("/logout")
def logout(request: Request) -> RedirectResponse:
    """
    Remove user from cache

    """
    id = request.session.pop("user", None)
    if id is not None:
        # TODO remove key from redis
        pass
    return RedirectResponse("/login")
