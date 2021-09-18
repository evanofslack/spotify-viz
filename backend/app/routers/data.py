from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import tekore as tk
from typing import List

from helpers.spotify import (
    get_display_name,
    get_currently_playing,
    get_last_played,
    get_spotify_id,
    get_playlist_ids,
    get_playlist_name,
    get_playlist_cover_image,
    get_playlist_songs)

from helpers.crud import (
    create_playlist,
    create_song,
    read_user,
    update_user,
    read_playlists)

from db.models import (
    UserOverview,
    UserUpdate,
    PlaylistCreate,
    SongCreate,
    PlaylistRead)

from helpers.tekore_setup import spotify, cred
from cache import cache

router = APIRouter(
    tags=["data"],
)


@router.get("/overview", response_model=UserOverview)
async def get_overview(request: Request):
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
            display_name = await get_display_name(spotify)
            current = await get_currently_playing(spotify)
            last = await get_last_played(spotify)

            user_overview = UserOverview(
                display_name=display_name,
                current_song=current["current_song"],
                current_artist=current["current_artist"],
                last_song=last["last_song"],
                last_artist=last["last_artist"],
                elapsed_time=last["elapsed_time"],
                time_units=last["time_units"]
            )

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}

    return user_overview


@router.get("/playlists")  # response_model=List[PlaylistRead]
async def get_playlists(request: Request):
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
            playlist_ids = await get_playlist_ids(spotify, spotify_id, limit=2)
            current_user = await read_user(spotify_id=spotify_id)

            if current_user.created_playlists:
                # update playlists
                playlists = await read_playlists(current_user.id)
                return playlists
            else:
                """ CREATE PLAYLISTS """
                for playlist_id in playlist_ids:
                    playlist_name = await get_playlist_name(spotify, playlist_id)
                    playlist_cover_image = await get_playlist_cover_image(
                        spotify, playlist_id)

                    new_playlist = PlaylistCreate(
                        playlist_id=playlist_id,
                        playlist_name=playlist_name,
                        playlist_cover_image=playlist_cover_image,
                        user_id=current_user.id,
                        user=current_user)

                    db_playlist = await create_playlist(new_playlist)
                    print("Created playlist: ", db_playlist.playlist_name)

                    """ CREATE SONGS """
                    # song_names, song_ids, artists = await get_playlist_songs(
                    #     spotify, playlist_id)

                    # for song_name, song_id, artist in zip(song_names, song_ids, artists):
                    #     new_song = SongCreate(song_id=song_id,
                    #                           song_name=song_name,
                    #                           artist=artist,
                    #                           playlist_id=db_playlist.id,
                    #                           playlist=new_playlist)
                    # db_song = await create_song(new_song)
                    # print("Created song: ", db_song.song_name)

                # update user.created_playlists
                playlists = await read_playlists(current_user.id)

                updated_user = await update_user(current_user.id,
                                                 UserUpdate(created_playlists=True))
                print(updated_user.created_playlists)
                return playlists

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}
