from APIs.Spotify import SpotifyAPIGateway
from APIs.IP import ipinfoAPI
from APIs.TicketMaster import TicketMasterAPIGateway
import os

#   Process for get_events()
# 1. Use IPInfoAPI to determine users loction

# 2. Use TicketMasterAPI to find events near users location

# 2.5 OPTIONAL: Either use TicketMaster 'ClassificationName' param to specify genre, or use SpotifyAPI to filter artists based on user reccomendations

# 3. Query Spotify API using events name as our search.
# an artist object is build as specced in SpotifyAPIGateway

# 4.   Process for create_playlist()
#   a. Spotify links to users account
#   b. Spotify finds top 5 songs by each artist
#   c. Spotify creates playlist


def get_events():

    # 1. locate users location
    ip = ipinfoAPI.find_ip()
    location = ipinfoAPI.find_ip_location(ip)
    
    # 2. find events
    ticketmaster = TicketMasterAPIGateway.TicketMasterAPIGateway()
    ticketmaster.events = ticketmaster.get_events(location.lat, location.long,) #city='Bristol')

    # 3. build artist objects 
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify = SpotifyAPIGateway.SpotifyAPIGateway(client_id, client_secret)
    spotify.token = spotify.get_token()

    for event in ticketmaster.events:
        print(event.name)
        artist_name = event.name
        artist = spotify.search_for_artist(artist_name)
        artist.catalog_objects = spotify.get_songs_by_artist(artist)
        artist.update_simple_catalog()
        artist_dict = artist.to_dict()
        print(f"The event is called {event.name}, where {artist.name} is playing at {event.venue.name} on {event.date}.")
        print(f"Here is some of their top songs:")
        for song in artist.catalog[:2]:
            print(song)

    # 4. Verify and filter artists

    # 5. Create user playlist


if __name__ == '__main__':      
    get_events()