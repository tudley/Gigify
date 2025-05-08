import requests

token = '80b1d0c600b786'
url = f"https://ipinfo.io?token={token}"
response = requests.get(url)
data = response.json()

print(data['city'])