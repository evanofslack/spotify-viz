import uvicorn
import tekore as tk
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="yeahyouthought")


file = 'tekore.cfg'
conf = tk.config_from_file(file)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)


@ app.get("/react")
def hello_react():
    return {"isLoggedIn": False, "username": "Evan"}


@ app.get("/home")
def read_root(request: Request):
    user = request.session.get('user', None)

    token = users.get(user, None)

    print('user: ', user)
    print('token: ', token)
    if user is None or token is None:
        request.session.pop('user', None)
        return {"isLoggedIn": False, "message": "Not logged in"}

    if token.is_expiring:
        token = cred.refresh(token)
        users[user] = token

    try:
        with spotify.token_as(token):
            display_name = spotify.current_user().display_name
            currently_playing = spotify.playback_currently_playing(
                tracks_only=True)
            if currently_playing:
                current_song = currently_playing.item.name
                current_artist = currently_playing.item.artists[0].name
            else:
                current_song, current_artist = None, None

    except tk.HTTPError as err:
        print(str(err))
        return {"error": "Could not fetch info"}
    return {"isLoggedIn": True,
            "display_name": display_name,
            "current_song": current_song,
            "current_artist": current_artist}


@ app.get("/login")
def login(request: Request):
    if 'user' in request.session:
        return RedirectResponse(url='/home')

    scope = tk.scope.user_read_currently_playing + \
        tk.scope.user_read_playback_state + tk.scope.user_read_recently_played
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    return {"url": auth.url}


@ app.get("/callback")
def login_callback(request: Request, code: str, state: str):

    auth = auths.pop(state, None)

    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)

    print("token: ", token)
    request.session['user'] = state
    users[state] = token
    return RedirectResponse('http://localhost:3000/')


@ app.get("/logout")
def logout(request: Request):
    uid = request.session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return RedirectResponse('/home')


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=5000, host='0.0.0.0', reload=True,
    )
