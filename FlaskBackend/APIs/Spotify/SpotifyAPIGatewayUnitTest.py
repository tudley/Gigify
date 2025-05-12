import unittest
from SpotifyAPIGateway import SpotifyAPIGateway, artist, Event

class SpotifyGatewayTest(unittest.TestCase):


    def setUp(self):
        return super().setUp()
    
    def test_get_token():
        # client id/secret invalid

        # client id/secret valid
        pass

    def test_get_auth_header():
        pass

    def search_for_artist():
        # no artist found

        # exact match found

        # spotify autocorrects search string
        
        pass

    def get_songs_by_artist():
        pass
