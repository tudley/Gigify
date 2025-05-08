import os
from requests import post, get
import base64
import json

from dotenv import load_dotenv

load_dotenv()

# here we fetch out client credentials from a seperate, secure .env file
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# THIS FILE GETS A TOKEN, SEARCHES FOR AN ARTIST, AND GETS THE ARTISTS TOP 10 SONGS

def get_token():
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

    # store out result, digging into the json response to extract useful information
    json_result = json.loads(result.content)['artists']['items']

    # if the search was unsuccessful, this block of code executes
    if len(json_result) == 0:
        print('no artists found...')
        return None
    
    # return the get request
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    """Find the top 10 songs in the UK of an artist from their ID previously found"""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UK"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


# this block we generate a token, query the API, store the ID of the result, and find the top songs of the artist using their ID
token = get_token()
#print(token)
result = search_for_artist(token, 'jazzbois')
#print(result)
artist_id = result['id']
#print(artist_id)
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}.{song['name']}")


# now, I want to get the data of a my profile


