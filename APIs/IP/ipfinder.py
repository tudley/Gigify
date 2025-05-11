import requests

def find_ip():
    ip = requests.get('https://api.ipify.org').text
    print(f"My public IP address is: {ip}")
    return ip