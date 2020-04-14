"""
Just a project made explores Spotify's API,
and analyzes the tracks of a user

Using the SpotifyAPI,
Spotipy for oauth,
matplotlib for graphing

Shows a graph of a user's playlist with the "mood" of it
"""
import json
import requests
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from secrets import spotify_user_id, spotify_token
from authorization import SpotifyCredentials


class GeneratePlaylist:
    def __init__(self):
        self.all_songs = {}

    def create_playlist(self):
        # Creates a new playlist
        request_body = json.dumps({
            "name": "GeneratedPlay",
            "description": "Playlist made with this dank app",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        # Return playlist ID
        return response_json["id "]

    def get_playlist_songs_uris(self, id, token):
        query = "	https://api.spotify.com/v1/playlists/{}/tracks".format(
            id
        )
        response = requests.get(
            query,
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer {}".format(token)
            }
        )
        response_json = response.json()
        song_uris = []
        for i in range(len(response_json['items'])):
            song_uris.append(
                response_json['items'][i]['track']['uri'][14:])
        return song_uris
    # searches for the song on spotify

    def get_spotify_uri(self, song_name, artist, token):
        # Searches for a song
        query = "https://api.spotify.com/v1/search?q=track%3A{}+artist%3A{}&type=track&limit=10&offset=5".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer {}".format(token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        uri = songs[0]["uri"]
        print(uri[14:])
        # spotify:track:3uFXxEURAepnTx1cZ51v4k
        return uri[14:]

    def get_analysis_features(self, song_id, token):

        query = "https://api.spotify.com/v1/audio-features/{}".format(
            song_id
        )
        response = requests.get(
            query,
            headers={
                "Content-type": "application/json",
                "Authorization": "Bearer {}".format(token)
            }
        )
        response_json = response.json()
        #  ex link of a track https://open.spotify.com/track/7nhWtCc3v6Vem80gYPlppQ?si=YhcLqAGPTviMrGZ2yoo12g
        analysis = {
            'valence': response_json['valence'],
            'energy': response_json['energy'],
            'danceability': response_json['danceability']
        }
        return analysis

    def add_songs(self):
        # Adding the songs to the playlist
        # get the uri
        uris = [info["spotify_uri"]for song, info in self.all_songs.items()]

        playlist_id = self.create_playlist()

        request_data = json.dumps(uris)

    def plot_analysis(self, stats):
        total_valence = 0
        total_danceability = 0
        total_energy = 0
        for i in range(len(stats)):
            total_valence += stats[i]['valence']
            total_energy += stats[i]['energy']
            total_danceability += stats[i]['danceability']

        avg_valence = total_valence/len(stats)
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        # print()
        # Plot some data on the axes.
        ax.plot([1, 2], [avg_valence, total_valence])
        plt.show()


if __name__ == '__main__':
    credentials = SpotifyCredentials()
    # print(credentials.get_token())
    cp = GeneratePlaylist()
    '''Request to get uri requires track and artist'''
    # song_uri = cp.get_spotify_uri(
    #     'Uptown Girl', 'Billy Joel', credentials.get_token())
    # cp.add_songs()
    #    def get_playlist(self, id, token):

    uris = cp.get_playlist_songs_uris(
        '4qZxNmnyXdK3vNIl9JSThg', credentials.get_token())

    '''valence is the musical positiveness of a track (ie happy as valence>)'''
    song_analysis = []
    for i in range(len(uris)):
        song_analysis.append(cp.get_analysis_features(
            uris[i], credentials.get_token()))
    print(song_analysis)
    cp.plot_analysis(song_analysis)
