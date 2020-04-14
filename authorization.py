import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2


CLIENT_ID = "80499bd993c1435fb442a56bfbe9f939"
CLIENT_SECRET = "5fed3fe23e7a42b6ac16451425dac965"


class SpotifyCredentials():
    def __init__(self):
        credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
        self.token = credentials.get_access_token()

    def get_token(self):
        return self.token
