import requests
import dotenv
import os

dotenv.load_dotenv()

class Location():
    def __init__(self, name, long, lat):
        self.name = name
        self.long = long
        self.lat = lat

def find_ip():
    ip = requests.get('https://api.ipify.org').text
    print(f"My public IP address is: {ip}")
    return ip


def find_ip_location(ip):
    """Find the Users location to the nearest city"""

    # Initiallise variables for the API call
    token = os.getenv('IPInfoAPI_token')
    url = f"https://ipinfo.io/{ip}?token={token}"

    # Get a response object and filter through its JSON to extract it's 'city' value
    response = requests.get(url)
    data = response.json()
    #print(data['loc'])
    lat_str, long_str = data['loc'].split(",")
    lat = float(lat_str)
    long = float(long_str)
    name = data['city']
    #long, lat = 1,1

    location = Location(name, long, lat)
    # Return 'city'
    return location

if __name__ == '__main__':
    ip = find_ip()
    location = find_ip_location(ip)
    print(location.long, location.lat)