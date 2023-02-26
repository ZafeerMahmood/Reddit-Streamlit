
import pandas as pd
from datetime import datetime
import requests
import streamlit as st
import os
from dotenv import load_dotenv
from components import chart, displayDf,makeBarChartBigrams,makeBarChartTrigrams
import altair as alt
from transformers import pipeline

load_dotenv()
st.set_page_config(layout='wide')
st.title('Dashboard for Reddit')

col1, col2, col3 = st.columns([0.4,2.5,0.4])
subreddit = "wallstreetbets" 

with st.container():
    with col1:
        st.markdown('#')
        subreddit = st.text_input('Enter subreddit name', subreddit)
        type =st.selectbox('select type?', ('hot', 'new',))
        limit =  st.selectbox(
            'select Limit?',
            ('50','100'))



#logic section
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
#logic section end

with st.container():
    with col2:
        st.write(f'{type} posts from {subreddit}')
        dataFrameOfRedditPosts=displayDf(res_hot)
        st.dataframe(dataFrameOfRedditPosts,use_container_width=True)

mean=dataFrameOfRedditPosts['Sentiment_score'].mean()
mean=round(mean,4)
avg=dataFrameOfRedditPosts['Sentiment'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'

avg.to_dict()

with st.container():
    with col3:
        st.markdown('#')
        st.write(f'Average Sentiment: ')
        st.write("Positive",avg['POS'])
        st.write("Negative",avg['NEG'])
        st.write("Neutural",avg['NEU'])
        st.write(f'mean Sentiment: {mean}')


cc1,cc2,cc3=st.columns([0.4,2.5,0.4])
with cc1:
    st.markdown('#')
    select='bitcoin'
    select = st.text_input('Enter coin name', select)
    interval = st.selectbox('Interval ?', (1,2,3))
with cc2:
    st.write(f'Chart of : {select}')
    pr=chart(select, interval)
with cc3:
    st.markdown('#')
    st.write(f'max price  is {round(pr[0])}')
    st.write(f'min price  is {round(pr[1])}')
    st.write(f'mean price  is {round(pr[2])}')

c1,c2,c3,c4=st.columns([0.2,1,1,0.2])

with c2:
    makeBarChartBigrams(dataFrameOfRedditPosts)
with c3:
    makeBarChartTrigrams(dataFrameOfRedditPosts)






