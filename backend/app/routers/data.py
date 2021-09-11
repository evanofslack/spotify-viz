from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import tekore as tk

from helpers.spotify import get_display_name, get_currently_playing, get_last_played
from helpers.tekore_setup import spotify, cred
from cache import cache

router = APIRouter(
    tags=["data"],
)


@router.get("/overview")
async def get_overview(request: Request):
    user = request.session.get('user', None)
    token = cache.users.get(user, None)

    if user is None or token is None:
        request.session.pop('user', None)
        return RedirectResponse(url='/login')

    if token.is_expiring:
        token = cred.refresh(token)
        cache.users[user] = token

    try:
        with spotify.token_as(token):
            display_name = await get_display_name(spotify)
            current = await get_currently_playing(spotify)
            last = await get_last_played(spotify)

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}

    return {"display_name": display_name,
            "current_song": current['current_song'],
            "current_artist": current['current_artist'],
            "last_song": last['last_song'],
            "last_artist": last['last_artist'],
            "elapsed_time": last['elapsed_time'],
            "time_units": last['time_units'],
            }
