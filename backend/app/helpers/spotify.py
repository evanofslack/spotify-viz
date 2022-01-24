import tekore as tk
import datetime
import iso8601
from typing import Dict, List, Tuple


async def get_spotify_id(spotify: tk.Spotify) -> str:
    """
    Get user's spotify ID

    """
    current_user = await spotify.current_user()
    spotify_id = current_user.id
    return spotify_id


async def get_display_name(spotify: tk.Spotify) -> str:
    """
    Get user's display name

    """
    current_user = await spotify.current_user()
    display_name = current_user.display_name
    return display_name


async def get_currently_playing(spotify: tk.Spotify) -> Dict:
    """
    Get user's current playback

    """
    currently_playing = await spotify.playback_currently_playing(tracks_only=True)
    if currently_playing and currently_playing.is_playing:
        current_song = currently_playing.item.name
        current_artist = currently_playing.item.artists[0].name
        current_image = currently_playing.item.album.images[0].url
    else:
        current_song, current_artist, current_image = None, None, None

    return {"current_song": current_song, "current_artist": current_artist, "current_image": current_image}


def elapsed_time_helper(elapsed_minutes: int) -> Tuple[int, str]:
    """
    Convert minutes to lowest time denomination

    """
    if elapsed_minutes < 2:
        elapsed_time = 1
        time_units = "minute"

    if elapsed_minutes >= 2 and elapsed_minutes < 60:
        elapsed_time = elapsed_minutes
        time_units = "minutes"

    if elapsed_minutes >= 60 and elapsed_minutes < 2*60:
        elapsed_time = round(elapsed_minutes / 60)
        time_units = "hour"

    if elapsed_minutes >= 2*60 and elapsed_minutes < 24*60:
        elapsed_time = round(elapsed_minutes / 60)
        time_units = "hours"

    if elapsed_minutes >= 24*60 and elapsed_minutes < 2*24*60:
        elapsed_time = round(elapsed_minutes / 60 / 24)
        time_units = "day"

    if elapsed_minutes >= 2*24*60:
        elapsed_time = round(elapsed_minutes / 60 / 24)
        time_units = "days"

    return elapsed_time, time_units


async def get_last_played(spotify: tk.Spotify) -> Dict:
    """
    Get user's last playback

    """
    play_history_paging = await spotify.playback_recently_played(limit=1)
    last_song = play_history_paging.items[0].track.name
    last_artist = play_history_paging.items[0].track.artists[0].name
    last_image = play_history_paging.items[0].track.album.images[0].url

    last_played_at = play_history_paging.items[0].played_at

    now_iso8601 = datetime.datetime.fromisoformat(datetime.datetime.now().astimezone().replace(
        microsecond=0).isoformat())
    last_played_at_parsed = iso8601.parse_date(str(last_played_at))
    elapsed_minutes = round((now_iso8601-last_played_at_parsed).seconds / 60)

    elapsed_time, time_units = elapsed_time_helper(elapsed_minutes)

    return {"last_song": last_song,
            "last_artist": last_artist,
            "last_image": last_image,
            "elapsed_time": elapsed_time,
            "time_units": time_units}


async def get_recent_genres(spotify: tk.Spotify, time_range: str = "short_term", num_artists: int = 20) -> List[str]:
    artists = await spotify.current_user_top_artists(time_range=time_range, limit=num_artists)

    genres = [genre for item in artists.items for genre in item.genres]

    return genres


async def get_playlist_ids(spotify: tk.Spotify, user_id: str, limit: int = 3) -> List[str]:
    """
    Get list of user's playlist IDs

    """
    playlist_paging = await spotify.playlists(user_id, limit)
    playlists = playlist_paging.items
    playlist_ids = [playlist.id for playlist in playlists]

    return playlist_ids


async def get_playlist_name(spotify: tk.Spotify, playlist_id: str) -> str:
    """
    Get playlist name from playlist ID

    """
    full_playlist = await spotify.playlist(playlist_id)
    return full_playlist.name


async def get_playlist_cover_images(spotify: tk.Spotify, playlist_id: str) -> List[str]:
    """
    Get playlist cover images from playlist ID

    """
    images = await spotify.playlist_cover_image(playlist_id)
    urls = [image.url for image in images]
    return urls


async def get_playlist_cover_image(spotify: tk.Spotify, playlist_id: str) -> str:
    """
    Get playlist cover image from playlist ID, returns the largest resolution image

    """
    images = await spotify.playlist_cover_image(playlist_id)
    url = images[0].url
    return url


async def get_playlist_songs(spotify: tk.Spotify, playlist_id: str) -> tuple[List[str], List[str], List[str]]:
    """
    Get all songs from a playlist

    """
    playlist_paging = await (spotify.playlist_items(
        playlist_id, as_tracks=False))

    playlist_generator = [spotify.all_items(playlist_paging)]

    for playlist in playlist_generator:
        items = [item async for item in playlist]

        song_names = [item.track.name for item in items]
        song_ids = [item.track.id for item in items]
        artists = [item.track.artists[0].name for item in items]

    return song_names, song_ids, artists
