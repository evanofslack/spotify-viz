from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import tekore as tk

from helpers.spotify import get_display_name, get_currently_playing, get_last_played

router = APIRouter(
    tags=["auth"],
)

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)

file = 'tekore.cfg'  # file = './app/tekore.cfg'
conf = tk.config_from_file(file)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()


@router.get("/is_logged_in")
def is_logged_in(request: Request):
    user = request.session.get('user', None)
    token = users.get(user, None)
    '''
    token = get_token_from_db(state: Str)
    '''

    if user is None or token is None:
        request.session.pop('user', None)
        return {"isLoggedIn": False, "message": "Not logged in"}
    else:
        return {"isLoggedIn": True}


@router.get("/overview")
def read_root(request: Request):
    user = request.session.get('user', None)
    token = users.get(user, None)

    if user is None or token is None:
        request.session.pop('user', None)
        return RedirectResponse(url='/login')

    if token.is_expiring:
        token = cred.refresh(token)
        users[user] = token

    try:
        with spotify.token_as(token):

            display_name = get_display_name(spotify)

            current = get_currently_playing(spotify)

            last = get_last_played(spotify)

    except tk.HTTPError as err:
        print(str(err))
        # print(err.response)
        # print(err.request)
        return {"error": "Could not fetch info"}
    return {"display_name": display_name,
            "current_song": current['current_song'],
            "current_artist": current['current_artist'],
            "last_song": last['last_song'],
            "last_artist": last['last_artist'],
            "elapsed_time": last['elapsed_time'],
            "time_units": last['time_units'],
            }


@router.get("/login")
def login(request: Request):
    if 'user' in request.session:
        return RedirectResponse(url='/home')

    scope = tk.scope.user_read_currently_playing + \
        tk.scope.user_read_playback_state + tk.scope.user_read_recently_played
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    '''
    update_user_db(auth.state, auth)
    '''
    return {"url": auth.url}


@router.get("/callback")
def login_callback(request: Request, code: str, state: str):

    auth = auths.pop(state, None)

    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)

    request.session['user'] = state
    users[state] = token
    return RedirectResponse('http://localhost:3000/')


@router.get("/logout")
def logout(request: Request):
    uid = request.session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return RedirectResponse('/login')
