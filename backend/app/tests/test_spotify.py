import tekore as tk
import pytest
from dotenv import load_dotenv
import os

from app.helpers.spotify import (
    get_spotify_id,
    get_display_name,
    get_currently_playing,
    elapsed_time_helper,
    get_last_played,
    get_playlist_ids,
    get_playlist_name,
    get_playlist_cover_image,
    get_playlist_cover_images,
    get_playlist_songs
)


@pytest.fixture
@pytest.mark.client
def tekore_client() -> tk.Spotify:
    load_dotenv()

    id = os.environ["SPOTIFY_CLIENT_ID"]
    secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    refresh = os.environ["SPOTIFY_USER_REFRESH"]
    token = tk.refresh_user_token(
        client_id=id, client_secret=secret, refresh_token=refresh)

    sender = tk.RetryingSender(sender=tk.AsyncSender())
    spotify = tk.Spotify(token=token, sender=sender, max_limits_on=True)
    return spotify


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_spotify_id(tekore_client):
    spotify_id = await get_spotify_id(tekore_client)
    await tekore_client.sender.close()
    assert spotify_id == "evan_slack"


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_display_name(tekore_client):
    display_name = await get_display_name(tekore_client)
    await tekore_client.sender.close()
    assert display_name == "Evan Slack"


@pytest.mark.asyncio
@pytest.mark.client
@pytest.mark.currently_playing
async def test_get_currently_playing(tekore_client):
    currently_playing = await get_currently_playing(tekore_client)
    await tekore_client.sender.close()

    assert type(currently_playing) is dict
    assert type(currently_playing["current_song"]) is str
    assert type(currently_playing["current_artist"]) is str
    assert type(currently_playing["current_image"]) is str


def test_elapsed_time_helper_min():
    elapsed_time, time_units = elapsed_time_helper(0)

    assert elapsed_time == 1
    assert time_units == "minute"


def test_elapsed_time_helper_mins():
    elapsed_time, time_units = elapsed_time_helper(59)

    assert elapsed_time == 59
    assert time_units == "minutes"


def test_elapsed_time_helper_hour():
    elapsed_time, time_units = elapsed_time_helper(60)

    assert elapsed_time == 1
    assert time_units == "hour"


def test_elapsed_time_helper_hours():
    elapsed_time, time_units = elapsed_time_helper(120)

    assert elapsed_time == 2
    assert time_units == "hours"


def test_elapsed_time_helper_day():
    elapsed_time, time_units = elapsed_time_helper(24*60)

    assert elapsed_time == 1
    assert time_units == "day"


def test_elapsed_time_helper_days():
    elapsed_time, time_units = elapsed_time_helper(2*24*60)

    assert elapsed_time == 2
    assert time_units == "days"


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_last_played(tekore_client):
    last_played = await get_last_played(tekore_client)
    await tekore_client.sender.close()

    assert type(last_played) is dict
    assert type(last_played["last_song"]) is str
    assert type(last_played["last_artist"]) is str
    assert type(last_played["last_image"]) is str
    assert type(last_played["elapsed_time"]) is int
    assert type(last_played["time_units"]) is str


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_playlist_ids(tekore_client):
    playlist_ids = await get_playlist_ids(tekore_client, user_id="evan_slack")
    await tekore_client.sender.close()

    assert type(playlist_ids) is list
    assert type(playlist_ids[0]) is str


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_playlist_name(tekore_client):
    playlist_name = await get_playlist_name(tekore_client, playlist_id="19LLssurgVr73eZz5kj2Ks")
    await tekore_client.sender.close()

    assert type(playlist_name) is str
    assert playlist_name == "auhgst"


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_playlist_cover_images(tekore_client):
    urls = await get_playlist_cover_images(tekore_client, playlist_id="19LLssurgVr73eZz5kj2Ks")
    await tekore_client.sender.close()

    assert type(urls) is list
    assert type(urls[0]) is str


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_playlist_cover_image(tekore_client):
    url = await get_playlist_cover_image(tekore_client, playlist_id="19LLssurgVr73eZz5kj2Ks")
    await tekore_client.sender.close()

    assert type(url) is str
    assert url == "https://mosaic.scdn.co/640/ab67616d0000b2731ddeb0fc6dd26b427bdbda20ab67616d0000b2736b8cc359a209e3dce188b993ab67616d0000b27370504af55d847f60cec4cbd7ab67616d0000b273f0ec272782698baa2381926a"


@pytest.mark.asyncio
@pytest.mark.client
async def test_get_playlist_songs(tekore_client):
    song_names, song_ids, artists = await get_playlist_songs(tekore_client, playlist_id="19LLssurgVr73eZz5kj2Ks")
    await tekore_client.sender.close()

    assert type(song_names) is list
    assert type(song_ids) is list
    assert type(artists) is list

    assert song_names[0] == "what i'm giving you"
    assert song_ids[0] == "2n6Klx7OcGsbnw68G4TI4T"
    assert artists[0] == "Sweeps"
