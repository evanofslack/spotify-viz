from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import tekore as tk

from helpers.tekore_setup import spotify, cred, scope
from helpers.spotify import get_spotify_id, get_playlist_ids, get_playlist_name, get_playlist_cover_image, get_playlist_songs
from helpers.crud import create_user, read_user, create_playlist, create_song

from db.models import UserCreate, PlaylistCreate, SongCreate
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
        playlist_ids = get_playlist_ids(spotify, spotify_id, limit=10)

        if read_user(spotify_id=spotify_id):
            print("User with ID: ", spotify_id, "already exists")
            # update_user
        else:
            """ CREATE USER """
            new_user = UserCreate(spotify_id=spotify_id)
            db_user = create_user(user=new_user)
            print("Created new user with ID: ", new_user.spotify_id)

            """ CREATE PLAYLISTS """
            for playlist_id in playlist_ids:
                playlist_name = get_playlist_name(spotify, playlist_id)
                playlist_cover_image = get_playlist_cover_image(
                    spotify, playlist_id)

                new_playlist = PlaylistCreate(
                    playlist_id=playlist_id,
                    playlist_name=playlist_name,
                    playlist_cover_image=playlist_cover_image,
                    user_id=db_user.id, user=new_user)

                db_playlist = create_playlist(new_playlist)
                print("Created playlist: ", db_playlist.playlist_name)

                """ CREATE SONGS """
                song_names, song_ids, artists = get_playlist_songs(
                    spotify, playlist_id)

                for song_name, song_id, artist in zip(song_names, song_ids, artists):
                    new_song = SongCreate(song_id=song_id,
                                          song_name=song_name,
                                          artist=artist,
                                          playlist_id=db_playlist.id,
                                          playlist=new_playlist)

                    db_song = create_song(new_song)
                    print("Created song: ", db_song.song_name)

    return RedirectResponse('http://localhost:3000/')


@ router.get("/logout")
def logout(request: Request):
    uid = request.session.pop('user', None)
    if uid is not None:
        cache.users.pop(uid, None)
    return RedirectResponse('/login')
