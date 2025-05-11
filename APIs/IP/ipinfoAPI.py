import requests
import dotenv
import os

dotenv.load_dotenv()

def get_city(ip):
    """Find the Users location to the nearest city"""

    # Initiallise variables for the API call
    token = os.getenv('IPInfoAPI_token')
    url = f"https://ipinfo.io/{ip}?token={token}"

    # Get a response object and filter through its JSON to extract it's 'city' value
    response = requests.get(url)
    data = response.json()

    # Return 'city'
    return data['city']