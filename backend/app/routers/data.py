from fastapi import APIRouter, Request, BackgroundTasks
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
    read_playlist,
    read_playlist_songs,
    update_user,
    read_playlists)

from db.models import (
    UserOverview,
    UserUpdate,
    PlaylistCreate,
    PlaylistOverview,
    SongCreate,
    PlaylistRead)

from helpers.tekore_setup import spotify, cred
from cache import cache

router = APIRouter(
    tags=["data"],
)


@router.get("/overview", response_model=UserOverview)
async def get_overview(request: Request):
    """
    Return overview of user's listening history

    """
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

            user_overview = UserOverview(
                display_name=display_name,
                current_song=current["current_song"],
                current_artist=current["current_artist"],
                current_image=current["current_image"],
                last_song=last["last_song"],
                last_artist=last["last_artist"],
                last_image=last["last_image"],
                elapsed_time=last["elapsed_time"],
                time_units=last["time_units"]
            )

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}

    return user_overview


@router.get("/playlists", response_model=List[PlaylistOverview])
async def get_playlists(request: Request, bg_tasks: BackgroundTasks):
    """
    Return a user's playlists. Initiate background task to save playlists to database

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
            playlist_ids = await get_playlist_ids(spotify, spotify_id, limit=10)
            current_user = await read_user(spotify_id=spotify_id)

            playlists, playlists_db = [], []
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

                new_playlist_db = PlaylistCreate(
                    playlist_id=playlist_id,
                    playlist_name=playlist_name,
                    playlist_cover_image=playlist_cover_image,
                    user_id=current_user.id,
                    user=current_user)
                playlists_db.append(new_playlist_db)

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}

    bg_tasks.add_task(create_db_playlists, playlists_db)
    bg_tasks.add_task(create_db_songs, token, playlists_db)
    return playlists


async def create_db_playlists(playlists: List[PlaylistCreate]) -> None:
    """
    Query database to see if playlist exists. If not, create the playlist. 

    """
    for playlist in playlists:
        playlist_read = await read_playlist(playlist.playlist_id)
        if not playlist_read:
            db_playlist = await create_playlist(playlist)
            print("Created playlist: ", db_playlist.playlist_name)

    return {"message": "created playlists"}


async def create_db_songs(token, playlists: List[PlaylistCreate]):
    """
    Query database to see if song exists in the correct playlist. If not, create the song. 

    """
    with spotify.token_as(token):
        for playlist in playlists:
            song_names, song_ids, artists = await get_playlist_songs(spotify, playlist.playlist_id)

            playlist_song_ids = [song.song_id for song in await read_playlist_songs(playlist.playlist_id)]

            for song_name, song_id, artist in zip(song_names, song_ids, artists):
                if song_id not in playlist_song_ids:
                    new_song = SongCreate(song_id=song_id,
                                          song_name=song_name,
                                          artist=artist,
                                          playlist_id=playlist.playlist_id,
                                          playlist=playlist)
                    db_song = await create_song(new_song)
                    print("Created song: ", db_song.song_name)
    # await spotify.sender.close()
    return {"message": "created songs"}
