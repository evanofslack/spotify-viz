import tekore as tk
import datetime
import iso8601
from typing import Dict, List


def get_spotify_id(spotify: tk.Spotify) -> str:
    spotify_id = spotify.current_user().id
    return spotify_id


def get_display_name(spotify: tk.Spotify) -> str:
    display_name = spotify.current_user().display_name
    return display_name


def get_currently_playing(spotify: tk.Spotify) -> Dict:
    currently_playing = spotify.playback_currently_playing(tracks_only=True)
    if currently_playing and currently_playing.is_playing:
        current_song = currently_playing.item.name
        current_artist = currently_playing.item.artists[0].name
    else:
        current_song, current_artist = None, None

    return {"current_song": current_song, "current_artist": current_artist}


def get_last_played(spotify: tk.Spotify) -> Dict:
    play_history_paging = spotify.playback_recently_played(limit=1)
    last_song = play_history_paging.items[0].track.name
    last_artist = play_history_paging.items[0].track.artists[0].name
    last_played_at = play_history_paging.items[0].played_at

    now_iso8601 = datetime.datetime.fromisoformat(datetime.datetime.now().astimezone().replace(
        microsecond=0).isoformat())
    last_played_at_parsed = iso8601.parse_date(str(last_played_at))
    elapsed_minutes = round((now_iso8601-last_played_at_parsed).seconds / 60)

    if elapsed_minutes < 60:
        elapsed_time = elapsed_minutes
        time_units = "minutes"

    if elapsed_minutes >= 60 and elapsed_minutes < 3600:
        elapsed_time = round(elapsed_minutes / 60)
        time_units = "hours"

    if elapsed_minutes >= 3600:
        elapsed_time = round(elapsed_minutes / 60 / 24)
        time_units = "days"

    return {"last_song": last_song,
            "last_artist": last_artist,
            "elapsed_time": elapsed_time,
            "time_units": time_units}


def get_playlist_ids(spotify: tk.Spotify, user_id: str, limit: int = 3) -> List[str]:
    playlist_paging = spotify.playlists(user_id, limit)
    playlists = playlist_paging.items
    playlist_ids = [playlist.id for playlist in playlists]

    return playlist_ids


def get_playlist_name(spotify: tk.Spotify, playlist_id: str) -> str:
    full_playlist = spotify.playlist(
        playlist_id)
    return full_playlist.name


def get_playlist_cover_images(spotify: tk.Spotify, playlist_id: str) -> List[str]:
    images = spotify.playlist_cover_image(playlist_id)
    urls = [image.url for image in images]
    return urls


def get_playlist_cover_image(spotify: tk.Spotify, playlist_id: str) -> str:
    images = spotify.playlist_cover_image(playlist_id)
    url = images[0].url
    return url


def get_playlist_songs(spotify: tk.Spotify, playlist_id: str) -> tuple[List[str], List[str], List[str]]:

    playlist_paging = spotify.playlist_items(
        playlist_id, as_tracks=False, limit=100)

    playlist_items = playlist_paging.items

    song_names = [item.track.name for item in playlist_items]
    song_ids = [item.track.id for item in playlist_items]
    artists = [item.track.artists[0].name for item in playlist_items]
    return song_names, song_ids, artists
