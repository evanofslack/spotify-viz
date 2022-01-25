import tekore as tk
from cache import cache
from db.models import UserOverview
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from helpers.spotify import get_currently_playing, get_display_name, get_last_played
from helpers.tekore_setup import cred, spotify

router = APIRouter(
    tags=["overview"],
)


@router.get("/overview", response_model=UserOverview)
async def get_overview(request: Request):
    """
    Return overview of user's listening history

    """
    user = request.session.get("user", None)
    token = cache.users.get(user, None)

    if user is None or token is None:
        request.session.pop("user", None)
        return RedirectResponse(url="/login")

    if token.is_expiring:
        token = cred.refresh(token)
        cache.users[user] = token

    try:
        with spotify.token_as(token):
            display_name = await get_display_name(spotify)
            current = await get_currently_playing(spotify)
            last = await get_last_played(spotify)

            user_overview = UserOverview(
                display_name=display_name,
                current_song=current["current_song"],
                current_artist=current["current_artist"],
                current_image=current["current_image"],
                last_song=last["last_song"],
                last_artist=last["last_artist"],
                last_image=last["last_image"],
                elapsed_time=last["elapsed_time"],
                time_units=last["time_units"],
            )

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}

    return user_overview
