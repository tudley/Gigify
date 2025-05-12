from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from APIs.Spotify.SpotifyAPIGateway import SpotifyAPIGateway
from APIs.TicketMaster import TicketMasterAPIGateway
import os
import urllib.parse

app = Flask(__name__)
CORS(app)

# temporary mock dictionary of events
events = [
    {
        'id' : 1,
        'name' : 'Radiohead',
        'venue' : 'colston hall', 
        'date' : '2025-06-01'
    },
    {
        'id' : 2,
        'name' : 'Slum Village',
        'venue' : 'SWX',
        'date' : '2025-05-20'

    }
]

@app.route("/") # decorator defines url which runs the function below
def home():
    string =  "<h1>Welcome to the backend of my Flask App</h1>" \
    "           <p>Please navigate through using url for now</p>" \
    "           <p>The following URLs are routed as API endpoints for my frontend: </p>" \
    "           <li> '/events/bristol' - please enter a city you'd like to query TicketMaster about" \
    "           <li> '/artists/pixies' - please enter an artist you'd like to query Spotify about"
    return string


@app.route("/artists/<artist_name>") 
def get_artist(artist_name):
    """Query the Spotify database for an artist, and return a JSON object of their details needed for web app"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify = SpotifyAPIGateway(client_id, client_secret)
    spotify.token = spotify.get_token()
    artist = spotify.search_for_artist(artist_name)
    artist.catalog_objects = spotify.get_songs_by_artist(artist)
    artist_dict = artist.to_dict()
    return jsonify(artist_dict)

@app.route('/test')
def test_combine():
    pass


@app.route("/events/<city>")
def get_events(city):
    events = TicketMasterAPIGateway.get_concerts(city)
    return jsonify(events)

@app.route("/login")
def login():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:5000/callback"
    scopes = "playlist-modify-public playlist-modify-private"

    
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": scopes
        })
    )

    return redirect(auth_url)

@app.route("/callback")
def callback():
    pass


if __name__ == "__main__":
    app.run(debug=True)


