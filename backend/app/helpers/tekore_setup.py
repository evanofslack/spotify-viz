import tekore as tk

file = 'tekore.cfg'  # file = './app/tekore.cfg'
conf = tk.config_from_file(file)
cred = tk.Credentials(*conf)
scope = tk.scope.user_read_currently_playing + \
    tk.scope.user_read_playback_state + tk.scope.user_read_recently_played

sender = tk.RetryingSender(sender=tk.AsyncSender())
spotify = tk.Spotify(sender=sender, max_limits_on=True)
