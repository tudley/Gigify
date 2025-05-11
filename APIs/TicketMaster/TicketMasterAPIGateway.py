import requests
import json
import dotenv
import os

dotenv.load_dotenv()

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

