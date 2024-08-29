import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
import random

# Replace with your Spotify client credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_youtube_link(song_name):
  """Searches for the song on YouTube and returns the first result's link."""
  query = f"https://www.youtube.com/results?search_query={song_name}"
  response = requests.get(query)
  soup = BeautifulSoup(response.content, 'html.parser')
  video_ids = soup.select("#video-results > ol > li > div.yt-lockup-video > div > div.yt-lockup-content > h3 > a")
  if video_ids:
      return f"https://www.youtube.com/watch?v={video_ids[0]['href'].split('=')[1]}"
  return None

def generate_song_list(num_songs=500):
  """Generates a list of songs with single-word names and their YouTube links."""
  songs = {}
  while len(songs) < num_songs:
    # Get a random playlist
    playlists = sp.search(q='playlist', type='playlist', limit=50)
    playlist = playlists['playlists']['items'][random.randint(0, 49)]
    playlist_tracks = sp.playlist_tracks(playlist['id'])

    for track in playlist_tracks['items']:
      song_name = track['track']['name']
      if ' ' not in song_name and len(song_name) > 2:
        # Check if the song name is a single word and has at least 3 characters
        youtube_link = get_youtube_link(song_name)
        if youtube_link:
          songs[song_name] = youtube_link
  return songs

# Generate the song list
song_list = generate_song_list()
print(song_list)