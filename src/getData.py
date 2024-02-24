import os
from dotenv import load_dotenv
import requests
import time
from transformers import pipeline
import pandas as pd

#hugging face model can be change to any trained model hosted on huggingface.co/models
specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis",)

def displayDf(url,header,type):
    responseReddit = requests.get(url, headers=header, params={'limit': 100})
    df_post_reddit=pd.DataFrame()
    # iterate over the posts to make a df to show
    for post in responseReddit.json()['data']['children']:
            df_post_reddit = df_post_reddit.append(
                {
                    'title': post['data']['title'],
                    'author_fullname': post['data']['author_fullname'],
                    'selftext': post['data']['selftext'],
                    'upvote_ratio': post['data']['upvote_ratio'],
                    'post_url': post['data']['url'],
                    'num_comments': post['data']['num_comments'],
                    'post_upvote': post['data']['ups'],
                    'link_flair_text': post['data']['link_flair_text'],
                    'Sentiment': specific_model(post['data']['title'])[0]['label'],
                    'Sentiment_score': specific_model(post['data']['title'])[0]['score'],
                }, ignore_index=True)
    df_post_reddit.to_csv(f'data_{type}.csv')


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