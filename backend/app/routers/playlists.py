from typing import List

import tekore as tk
from cache import cache
from db.crud import read_user
from db.models import PlaylistOverview
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from helpers.spotify import (
    get_playlist_cover_image,
    get_playlist_ids,
    get_playlist_name,
    get_playlist_songs,
    get_spotify_id,
)
from helpers.tekore_setup import cred, spotify

router = APIRouter(
    tags=["playlists"],
)


@router.get("/playlists", response_model=List[PlaylistOverview])
async def get_playlists(request: Request, bg_tasks: BackgroundTasks):
    """
    Return a user's playlists

    """
    user = request.session.get('user', None)
    token = cache.users.get(user, None)

    if user is None or token is None:
        request.session.pop('user', None)
        return RedirectResponse(url='/login')

    if token.is_expiring:
        token = await cred.refresh(token)
        cache.users[user] = token

    try:
        with spotify.token_as(token):
            spotify_id = await get_spotify_id(spotify)
            playlist_ids = await get_playlist_ids(spotify, spotify_id, limit=15)

            playlists = []
            for playlist_id in playlist_ids:
                playlist_name = await get_playlist_name(spotify, playlist_id)
                playlist_cover_image = await get_playlist_cover_image(
                    spotify, playlist_id)

                new_playlist = PlaylistOverview(
                    playlist_id=playlist_id,
                    playlist_name=playlist_name,
                    playlist_cover_image=playlist_cover_image
                )
                playlists.append(new_playlist)

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}

    return playlists

