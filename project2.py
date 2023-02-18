
import pandas as pd
from datetime import datetime
import requests
import streamlit as st
import os
from dotenv import load_dotenv
from components import chart, displayDf, rating

load_dotenv()

st.title('Dashboard for Reddit')
st.write('This is a simple app to get the hot posts from the subreddit of your choice')

subreddit = "wallstreetbets"
type =st.selectbox('select type?', ('hot', 'new',))
limit = st.selectbox(
    'select Limit?',
    ('10', '20', '30'))

secret_key = os.getenv('secret_key')
client_id = os.getenv('client_id')
auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
print(auth)

login_data = {
    'grant_type': 'password',
    'username': os.getenv('nameForReddit'),
    'password': os.getenv('password')
}

headers = {'User-Agent': 'MyAPI/0.0.1'}
response = requests.post('https://www.reddit.com/api/v1/access_token',
                         auth=auth, data=login_data, headers=headers) # user auth to get the token for reddit API

token = response.json()['access_token']
header = {"Authorization": f"bearer {token}", "User-Agent": "'MyAPI/0.0.1'"}

res_hot = requests.get(
    f'https://oauth.reddit.com/r/{subreddit}/{type}', headers=header, params={'limit': limit}) # get the hot/new posts from the subreddit


df_hot_posts = pd.DataFrame()

st.write(f'{type} posts from {subreddit}')

st.dataframe(displayDf(res_hot, df_hot_posts),use_container_width=True)


select = st.selectbox('Cryptocurrency ?', ('bitcoin', 'ethereum',))
interval = st.selectbox('Interval ?', (1,2,3))
st.write(f'Chart of : {select}')
st.button('Show Chart',on_click=chart(select, interval))

textRate=pd.DataFrame()

for post in res_hot.json()['data']['children']:
    if(post['data']['selftext'] == ''): # if the post has no text, skip it
        continue
    textRate = textRate.append(
        {
            'Text': post['data']['selftext'],
            'positivity Rating': rating(post['data']['selftext']),
        }, ignore_index=True)

st.dataframe(textRate)