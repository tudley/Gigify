import requests
import json

# THIS takes the outcome of IpInfoAPI (Stirng of a city), and finds concerts nearby through TicketMaster API

consumer_key = "uGKMJdMYV68qye1o5aZPOxTcPWRgXjUa"
consumer_secret = "Dunun7CAtoWxtn1h"

url = 'https://app.ticketmaster.com/discovery/v2/events.json'

city = 'Bristol' # use ipinfp api to get city

params = {
    'apikey' : consumer_key,
    'city' : city,
    'classificationName' : 'jazz',
    'size' : 10
}

response = requests.get(url, params=params)

if response.status_code == 200:
    events = response.json()
    print(events.keys())
    print(events['_embedded'].keys())
    print(events['_embedded']['events'][0].keys())

    for event in events['_embedded']['events']:
        print(event['name'])

print(response.status_code)

