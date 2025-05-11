from APIs.Spotify import SpotifyAPIGateway
from APIs.IP import ipinfoAPI, ipfinder
from APIs.TicketMaster import TicketMasterAPIGateway

#   Process for get_events()
# 1. Use IPInfoAPI to determine users loction

# 2. Use TicketMasterAPI to find events near users location

# 2.5 OPTIONAL: Either use TicketMaster 'ClassificationName' param to specify genre, or use SpotifyAPI to filter artists based on user reccomendations

# 3. Verify Artists vs Spotify catalog:
#   if event name == artist name, artist is verified 
#       (ie. 'The Jam' == 'The Jam', adds artist to list)
#   if event name != artist name but spotify returns result, user can confirm/deny equality 
#       (user confirms 'The Strokes Live in Bristol' == 'The Strokes, adds artist to list)
#       (user declines 'The Smiths tribute band' != 'The Smiths', artist is disregarded)
#   if spotify doesnt return a result for artist name, artist is disregarded
#       (artist name 'Local man plays tuba' returns no result in spotify API, artist is disregarded)


#   Process for create_playlist()
# 1. Spotify links to users account
# 2. Spotify finds top 5 songs by each artist
# 3. Spotify creates playlist

def get_events():

    # 1. locate users location
    ip = ipfinder.find_ip()
    city = ipinfoAPI.get_city(ip)

    # 2. find events
    events = TicketMasterAPIGateway.get_concerts(city)
