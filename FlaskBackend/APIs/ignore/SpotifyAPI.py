import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Provide your app credentials so spotify knows its you:

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="05a9da9f9f3647c18714e8b9226bc57d",
        client_secret="2bfd370aee3b4a04b42ba355118a773c")
    )

result = sp.artist("53KwLdlmrlCelAZMaLVZqU")

for attribute in result:
    print(attribute)

