import tekore as tk
from helpers.spotify import get_spotify_id, get_playlist_songs, get_playlist_ids, get_playlist_name, get_playlist_cover_image
from helpers.tekore_setup import spotify

from db.models import PlaylistCreate, Playlist
from db.models import UserCreate, User
from db.database import Session, engine, create_db_and_tables

create_db_and_tables()

with Session(engine) as session:
    user_1 = User(spotify_id="evan")
    playlist_1 = Playlist(playlist_id="playlistID1",
                          user_id=user_1.id, user=user_1)

    playlist_2 = Playlist(playlist_id="playlistID2",
                          user_id=user_1.id, user=user_1)

    # Something is wrong with my session creation
    # db_user_1 = User.from_orm(user_1)
    # db_playlist_1 = Playlist.from_orm(playlist_1)
    # db_playlist_2 = Playlist.from_orm(playlist_2)

    # session.add(user_1)
    session.add(playlist_1)
    session.add(playlist_2)
    session.commit()
    session.refresh(playlist_1)
    session.refresh(playlist_2)
    # session.refresh(user_1)

    print("created playlist: ", playlist_1.playlist_id)
    print("with user: ", playlist_1.user.spotify_id)


file = 'tekore.cfg'
conf = tk.config_from_file(file, return_refresh=True)
token = tk.refresh_user_token(*conf[:2], conf[3])
spotify = tk.Spotify(token)


spotify = tk.Spotify(token)

spotify_id = get_spotify_id(spotify)
playlist_ids = get_playlist_ids(spotify, spotify_id)

for id in playlist_ids:
    playlist_name = get_playlist_name(spotify, id)
    songs, artists = get_playlist_songs(spotify, id)
    urls = get_playlist_cover_image(spotify, id)
    print("\n")
    print("Playlist: ", playlist_name)
    for url in urls:
        print(url)

for song, artist in zip(songs, artists):
    print(song, "by: ", artist)
