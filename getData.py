import os
from dotenv import load_dotenv
from components import displayDf
import requests
import time

load_dotenv()

subreddit = "wallstreetbets"

secret_key = os.getenv('secret_key')
client_id = os.getenv('client_id')
auth = requests.auth.HTTPBasicAuth(client_id, secret_key)

login_data = {
    'grant_type': 'password',
    'username': os.getenv('nameForReddit'),
    'password': os.getenv('password')
}

headers = {'User-Agent': 'MyAPI/0.0.1'}
response = requests.post('https://www.reddit.com/api/v1/access_token',
                         auth=auth, data=login_data, headers=headers)

token = response.json()['access_token']
header = {"Authorization": f"bearer {token}", "User-Agent": "'MyAPI/0.0.1'"}


url_hot=f'https://oauth.reddit.com/r/{subreddit}/hot'
url_new=f'https://oauth.reddit.com/r/{subreddit}/new'



while True:
    displayDf(url_hot,header,'hot')
    displayDf(url_new,header,'new')
    time.sleep(300)#5 minutes