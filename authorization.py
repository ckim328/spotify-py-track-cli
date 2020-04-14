import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2


CLIENT_ID = ""
CLIENT_SECRET = ""


class SpotifyCredentials():
    def __init__(self):
        credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
        self.token = credentials.get_access_token()

    def get_token(self):
        return self.token
