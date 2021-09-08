import tekore as tk
from helpers.spotify import get_spotify_id, get_playlist_songs, get_playlist_ids, get_playlist_name, get_playlist_cover_image
from helpers.tekore_setup import spotify

file = 'tekore.cfg'
conf = tk.config_from_file(file, return_refresh=True)
token = tk.refresh_user_token(*conf[:2], conf[3])
spotify = tk.Spotify(token)


spotify = tk.Spotify(token)

user_id = get_spotify_id(spotify)
playlist_ids = get_playlist_ids(spotify, user_id)

for id in playlist_ids:
    playlist_name = get_playlist_name(spotify, id)
    songs, artists = get_playlist_songs(spotify, id)
    urls = get_playlist_cover_image(spotify, id)
    print("\n")
    print("Playlist: ", playlist_name)
    for url in urls:
        print(url)

    # for song, artist in zip(songs, artists):
    #     print(song, "by: ", artist)
