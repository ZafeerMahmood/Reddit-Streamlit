
import pandas as pd
from datetime import datetime
import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


st.title('Dashboard for Reddit')
st.write('This is a simple app to get the hot posts from the subreddit of your choice')

subreddit = st.selectbox(
    'select Subreddit?',
    ('wallstreetbets', 'games', ))

st.write('You selected:', subreddit)


limit = st.selectbox(
    'select Limit?',
    ('10', '20','30' ))


secret_key = os.getenv('secret_key')
client_id = os.getenv('client_id')

auth = requests.auth.HTTPBasicAuth(client_id,secret_key)
print(auth)


login_data = {
    'grant_type':'password',
    'username':os.getenv('nameForReddit'),
    'password':os.getenv('password')
}

headers = {'User-Agent': 'MyAPI/0.0.1'}
response = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth,data=login_data, headers=headers)
token = response.json()['access_token']
header = {"Authorization": f"bearer {token}", "User-Agent": "'MyAPI/0.0.1'"}

#{wallstreetbets}
res_hot = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot',headers=header,params={'limit':limit})

post = res_hot.json()['data']['children'][0]

# [i for i in post['data'].keys()]
df_hot_posts = pd.DataFrame()

for post in res_hot.json()['data']['children']:
    df_hot_posts = df_hot_posts.append(
                           {'subreddit' : post['data']['subreddit'],
                 'author_fullname': post['data']['author_fullname'],
   'created at': datetime.utcfromtimestamp(post['data']['created']),
                                     'title': post['data']['title'],
                               'selftext': post['data']['selftext'],
                       'upvote_ratio': post['data']['upvote_ratio'],
                      'Post ID':post['kind']+'_'+post['data']['id']
                      
                            }, ignore_index=True)
    #[[i] for i in df_hot_posts['title']]

st.table(df_hot_posts)