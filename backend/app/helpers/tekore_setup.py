import tekore as tk

file = 'tekore.cfg'  # file = './app/tekore.cfg'
conf = tk.config_from_file(file)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()
scope = tk.scope.user_read_currently_playing + \
    tk.scope.user_read_playback_state + tk.scope.user_read_recently_played
