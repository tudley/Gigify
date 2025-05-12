import requests
import json
import dotenv
import os

dotenv.load_dotenv()

class Venue():
    def __init__(self, name, id, long, lat, address):
        self.name = name
        self.id = id
        self.long = long
        self.lat = lat
        self.address = address

class Event():
    def __init__(self, name, venue, date):
        self.name = name
        self.artist = None
        self.venue = venue
        self.date = date

    def to_dict(self):
        if self.artist != None:
            return {
                "name": self.name,
                "artist": self.artist.name,
                "venue": self.venue,
                "date" : self.date,
            }
        else:
            return{
                "name": self.name,
                "artist": self.artist,
                "venue": self.venue,
                "date" : self.date,
            }

class TicketMasterAPIGateway():
    """This class provides the 'get_events() method, which returns a list of Event objects based of query"""
    def __init__(self):
        self.consumer_key = os.getenv('TicketMaster_consumer_key')
        self.url = 'https://app.ticketmaster.com/discovery/v2/events.json'
        self.events = []
        self.venues = []
        self.size = 10
        self.radius = 15
        self.unit = 'miles'

        self.params = {
            'apikey' : self.consumer_key,
            'classificationName' : 'music',
            'size' : self.size,
            'radius' : self.radius,
            'unit' : self.unit
        }

    def update_params_latlong(self, lat, long , radius=20, unit='miles'):
        """Adjust the search parameters"""
        self.params['radius'] = radius
        self.params['unit'] = unit
        if lat and long:
            self.params['city'] = None
            self.params['latlong'] = f"{lat},{long}"

    def update_params_city(self, city,radius=20, unit='miles'):
        """Adjust the search parameters"""
        self.params['radius'] = radius
        self.params['unit'] = unit
        if city:
            self.params['city'] = city
            self.params['latlong'] = None

    def check_new_venue(self, venue_name):
        for venue in self.venues:
            if venue_name == venue.name:
                return venue
        return False
    
    def parse_response(self, events):
        list_of_event_objects = []
        for event_data in events['_embedded']['events']:
            #print(event_data['_embedded']['venues'][0])
        #print(f"{event['name']} playing at {event['_embedded']['venues'][0]['name']}" + 
            #f"on {event['dates']['start']['dateTime']}")

            # event details
            event_name = event_data['name']
            event_time = event_data['dates']['start']['dateTime']

            # venue details
            venue_data = event_data['_embedded']['venues'][0]

            venue_name = venue_data.get('name', 'unknown')
            venue_id = venue_data.get('id', 'unknown')
            venue_location = venue_data.get('location')
            if venue_location:
                venue_long = venue_location['longitude']
                venue_lat = venue_location['latitude']
            venue_address = venue_data.get('address')

            # create new venue if no venue exists with matching values
            venue = self.check_new_venue(venue_name)
            if not venue:
                venue = Venue(venue_name, venue_id, venue_long, venue_lat, venue_address)
                self.venues.append(venue)
            event_obj =Event(event_name, venue, event_time)
            list_of_event_objects.append(event_obj)
        return list_of_event_objects
            

    def get_events(self, lat, long, city=None, radius=15, unit='miles'):
        """Return a List of Event objects based on events happening local
            to the user within a month from now"""
        
        # if user provides a city, use that, otherwise use default of users IP LatLong
        if city:
            self.update_params_city(city, radius, unit)
        else:
            self.update_params_latlong(lat, long, radius, unit)

        response = requests.get(self.url, params=self.params)

        # If the request was successful, filter the artist names out of the response, and add it to an empty list
        if response.status_code == 200:
            events = response.json()
            list_of_event_objects = self.parse_response(events)
            return list_of_event_objects
        
        # if request fails, return an empty list
        else:
            print('request failed')
            return []


if __name__ == '__main__':
    ticketmaster = TicketMasterAPIGateway()
    lat, long = 51.5407,-2.4184

    # default query, no city info used
    ticketmaster.events = ticketmaster.get_events(lat, long)
    for event in ticketmaster.events:
        print(f"{event.name} playing at {event.venue.name} on {event.date}")

    # query where user manually inputs city:
    ticketmaster.events = ticketmaster.get_events(lat, long, 'Brighton')
    for event in ticketmaster.events:
        print(f"{event.name} playing at {event.venue.name} on {event.date}")
    

# THIS takes the outcome of IpInfoAPI (Stirng of a city), and finds concerts nearby through TicketMaster API

def get_concerts(city):

    # Initialise some variables for the API and the URL access point
    consumer_key = os.getenv('TicketMaster_consumer_key')
    consumer_secret = os.getenv('TicketMaster_consumer_secret')
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    # Pass our variables into the parameters key of the request
    params = {
        'apikey' : consumer_key,
        'city' : city,
        'classificationName' : 'music',
        'size' : 100
    }

    # Interface with TicketMasters API and get the response object
    response = requests.get(url, params=params)

    # If the request was successful, filter the artist names out of the response, and add it to an empty list
    if response.status_code == 200:
        events = response.json()

        #print(events.keys())
        #print(events['_embedded'].keys())
        #print(events['_embedded']['events'][0].keys())

        return_events = []
        for event in events['_embedded']['events']:
            return_events.append(event['name'])

    return(return_events)

