import tekore as tk


CLIENT_ID = 'd7d15d88b7ae42efb087584ef247e6c4'
CLIENT_SECRET = '262706ce2c8946e0974c29a5e8fc3d26'
REDIRECT_URI = 'http://localhost:5000/callback'

conf = (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
file = 'tekore.cfg'

token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
tk.config_to_file(file, conf + (token.refresh_token))
