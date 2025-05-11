import os
from requests import post, get
import base64
import json

from dotenv import load_dotenv

load_dotenv()

class Artist():
    def __init__(self, name, id, verified = False):
        self.name = name
        self.id = id
        self.verified = verified
        self.catalog_objects = []
        self.catalog = []

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "verified": self.verified,
            "catalog" : self.catalog,
        }
    
    def update_simple_catalog(self):
        self.catalog = []
        for object in self.catalog_objects:
            song = {}
            song['name'] = object['name']
            song['id'] = object['id']
            self.catalog.append(song)


class Event():
    def __init__(self, artist, venue, date):
        self.artist = artist
        self.venue = venue
        self.date = date

class SpotifyAPIGateway():
    def __init__(self, client_id, client_secret, token=None, headers=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.headers = headers

    def get_token(self):
        """Here we are generating and returning our token to access the spotify web API
            Spotify required a base64 encoded string of "client_id:client_secret" """
        
        # here we build & encode the string 
        auth_string = self.client_id + ':' + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        # declare the url we are going to interface with
        url = "https://accounts.spotify.com/api/token"

        # the headers and data attributes of the post request are defined here:
        headers = {
            "Authorization" : "Basic " + auth_base64,
            "Content-Type" : "application/x-www-form-urlencoded"
            }
        data = {"grant_type" : "client_credentials"}

        # lets upload our credentials to the spotify API to generate our token
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result['access_token']
        return token
        
    
    def get_auth_header(self):
        """Once you have been authenticated, the header you want is different, as follows:"""
        return {"Authorization" : "Bearer " + self.token}


    def search_for_artist(self, artist):
        """Here we search for an artist by a string"""

        # here is the url we want to interface with
        url = 'https://api.spotify.com/v1/search'

        # generate the headers for the request through the previous function
        self.headers = self.get_auth_header()

        # here we create a query URL, limiting the results to type=artist and limit=1
        query = f"q={artist}&type=artist&limit=1"
        query_url = url + '?' + query

        # get the results through a get request
        result = get(query_url, headers=self.headers)
        #print(result.json()['artists']['items'][0])

        # store out result, digging into the json response to extract useful information
        json_result = json.loads(result.content)['artists']['items'][0]

        # if the search was unsuccessful, this block of code executes
        if len(json_result) == 0:
            print('no artists found...')
            return None
        
        # if the query 'name' value matches the string 'artist' argument, build artist object accordingly
        if json_result['name'].lower().strip() == artist.lower().strip():
            artist = Artist(json_result['name'], json_result['id'], verified = True)
        # if the query 'name' value doesn't exactly match the string 'artist' argument, build artist object accordingly
        else:
            artist = Artist(json_result['name'], json_result['id'])
        return artist


        
    def get_songs_by_artist(self, artist):
        """Find the top 10 songs in the UK of an artist from their ID previously found"""
        url = f"https://api.spotify.com/v1/artists/{artist.id}/top-tracks?country=UK"
        self.headers = self.get_auth_header()
        result = get(url, headers=self.headers)
        json_result = json.loads(result.content)['tracks']
        return json_result
    
    



if __name__ == "__main__":

    # OOP Approach
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify = SpotifyAPIGateway(client_id, client_secret)
    spotify.token = spotify.get_token()
    artist = spotify.search_for_artist('The Prodigy')
    artist.catalog_objects = spotify.get_songs_by_artist(artist)
    artist.update_simple_catalog()
    artist_dict = artist.to_dict()
    print(artist_dict)






def get_token(client_id, client_secret):
    """Here we are generating and returning our token to access the spotify web API
        Spotify required a base64 encoded string of "client_id:client_secret" """
    # here we build the string 
    auth_string = client_id + ':' + client_secret
    # and now we encode it
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    # declare the url we are going to interface with
    url = "https://accounts.spotify.com/api/token"
    # the headers and data attributes of the post request are defined here:
    # headers 
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    # lets upload our credentials to the spotify API to generate our token
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    # extract just the token, end return it
    token = json_result['access_token']
    return token

def get_auth_header(token):
    """Once you have been authenticated, the header you want is different, as follows:"""
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist):
    """Here we search for an artist by a string"""
    # here is the url we want to interface with
    url = 'https://api.spotify.com/v1/search'
    # generate the headers for the request through the previous function
    headers = get_auth_header(token)
    # here we create a query, limiting the results to type=artist and limit=1
    query = f"q={artist}&type=artist&limit=1"
    # now rebuild the url with our bespoke query
    query_url = url + '?' + query
    # get the results through a get request
    result = get(query_url, headers=headers)
    #print(result.json()['artists']['items'][0])
    # store out result, digging into the json response to extract useful information
    json_result = json.loads(result.content)['artists']['items'][0]
    # if the search was unsuccessful, this block of code executes
    if len(json_result) == 0:
        print('no artists found...')
        return None
    # if the query 'name' value matches the string 'artist' argument, confirm exact match
    if json_result['name'] == artist:
        match = True
    # if the query 'name' value does not exactly match the string 'artist' argument, user can confirm/dismiss spotifys match
    else:
        user_response = input(f'Spotify has equated the artist {artist} to {json_result['name']} - is this correct? (y/n)').strip().lower()
        if user_response == 'y':
            match = True
        elif user_response == 'n':
            match = False
        print(f'User has determined the match to be {match}')
    if match == True:
        # return the get request as a dictionary of information we need:
        response_dict = {}
        response_dict['name'] = json_result['name']
        response_dict['id'] = json_result['id']
        return response_dict

def get_songs_by_artist(token, artist_id):

    """Find the top 10 songs in the UK of an artist from their ID previously found"""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UK"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def procedurally_execute_code():
    # Procedural approach
    # here we fetch out client credentials from a seperate, secure .env file
    #client_id = os.getenv('SPOTIFY_CLIENT_ID')
    #client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # this block we generate a token, query the API, store the ID of the result, and find the top songs of the artist using their ID
    #token = get_token(client_id, client_secret)
    #print(token)
    #artist = search_for_artist(token, 'u3')
    #print(result)
    #if artist:
    #    artist_id = artist['id']
    #    print(artist_id)
    #    songs = get_songs_by_artist(token, artist_id)

    #    for idx, song in enumerate(songs):
    #        print(f"{idx + 1}.{song['name']}")
    pass