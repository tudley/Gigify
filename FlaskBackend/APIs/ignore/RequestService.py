import requests

data = {
        'name' : 'Skream',
        'venue' : 'Trinity Center',
        'date' : '2025-05-11'
}

res = requests.post("http://127.0.0.1:5000/events", json=data)

print(res.status_code)
print("Response Text:", res.text)