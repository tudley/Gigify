import requests
from requests.exceptions import HTTPError
import json
import dotenv
import os
import base64

dotenv.load_dotenv()

# URLS = ["https://api.github.com", "https://api.github.com/invalid"]
# for url in URLS:
    # try:
        # response = requests.get(url)
        # response.raise_for_status()
    # except HTTPError as http_err:
        # print(f"HTTP error occured: {http_err}")
    # except Exception as err:
        # print(f"Other error occured: {err}")
    # else:
        # print('success')


r = requests.get('https://api.github.com')

# check success of get request
if r:
    print('success')
else:
    raise Exception(f'fail - status code: {r.status_code}')

# read content of get request
text = r.text
print(text)

# read it as a json
json_response = r.json()
print(json_response['current_user_url'])

# HEADERS 
print(r.headers)

url1 = 'https://github.com/search?q=proxy&type=repositories'
# QUERYING Github:
r = requests.get('https://api.github.com/search/repositories',
                 params = {'q' : 'language:python', 'sort' : 'stars', 'order' : 'desc'})
r_json = r.json()
repos = r_json['items']
for repo in repos[:3]:
    print(f'name = {repo['name']}')
    print(f'desc = {repo['description']}')
    print(f'stars = {repo['stargazers_count']}')

url2 = 'https://api.github.com/search/repositories'
r2 = requests.get(url2, 
                  params = {"q" : '"real python"'},
                  headers = {"Accept" : "application/vnd.github.text-match+json"})
json_response = r2.json()
first_repo = json_response['items'][0]
print(first_repo['text_matches'][0]['matches'])

# interacting with my own repos
token = os.getenv('token')
#print(token)
repo_owner = 'tudley'
repo_name = 'TopInterview150'
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
headers = {'Authorization' : f"token {token}",
           }

my_repo = requests.get(url, headers=headers)

if my_repo.status_code == 200:
    print('success')
    json_repo = my_repo.json()
    #for file in json_repo:
        #print(file['name'] + ' - ' + file['type'])
        #content = base64.b64decode(file)
else:
    print(f'error - repo not found - {my_repo.status_code}')