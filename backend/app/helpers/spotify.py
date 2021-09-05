import tekore as tk
import datetime
import iso8601
from typing import Dict


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
