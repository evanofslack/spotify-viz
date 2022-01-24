import asyncio
import tekore as tk
from dotenv import load_dotenv


from helpers.spotify import get_spotify_id, get_playlist_songs, get_playlist_ids, get_playlist_name, get_playlist_cover_image, get_recent_genres
from helpers.tekore_setup import spotify
from db.models import PlaylistCreate, Playlist, UserCreate, User, Song
from db.database import engine

# create_db_and_tables()

# with Session(engine) as session:
#     user_1 = User(spotify_id="evan")

#     playlist_1 = Playlist(playlist_id="playlistID1",
#                           playlist_name="name",
#                           playlist_cover_image="image",
#                           user_id=user_1.id, user=user_1)

#     song_1 = Song(song_id="id",
#                   song_name="name",
#                   artist="artist",
#                   playlist_id=playlist_1.id,
#                   playlist=playlist_1)

#     # Something is wrong with my session creation
#     # db_user_1 = User.from_orm(user_1)
#     # db_playlist_1 = Playlist.from_orm(playlist_1)
#     # db_playlist_2 = Playlist.from_orm(playlist_2)

#     # session.add(user_1)
#     session.add(playlist_1)
#     session.add(song_1)
#     session.commit()
#     session.refresh(playlist_1)
#     session.refresh(song_1)
#     # session.refresh(user_1)

#     print("created playlist: ", playlist_1.playlist_id)
#     print("with user: ", playlist_1.user.spotify_id)


async def main():
    load_dotenv()
    conf = tk.config_from_environment(return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])

    sender = tk.RetryingSender(sender=tk.AsyncSender())
    spotify = tk.Spotify(sender=sender, max_limits_on=True)

    with spotify.token_as(token):

        genres = await get_recent_genres(spotify, num_artists=50)
        print(len(genres))
        for genre in genres:
            print(genre)

        # spotify_id = await get_spotify_id(spotify)
        # playlist_ids = await get_playlist_ids(spotify, spotify_id, limit=2)

        # for id in playlist_ids:
        #     playlist_name = await get_playlist_name(spotify, id)
        #     print("Playlist: ", playlist_name)

        #     song_names, song_ids, artists = await get_playlist_songs(spotify=spotify, playlist_id=id)

        #     for song, song_id, artist in zip(song_names, song_ids, artists):
        #         print(song, "by: ", artist)
        #         print(song_id)

    await sender.close()

if __name__ == "__main__":
    asyncio.run(main())


# https://github.com/python-poetry/poetry/issues/536
