import requests
import pandas as pd
import streamlit as st
import altair as alt
from textblob import TextBlob




def chart(select, selectInterval):
    endpoint = f'https://api.coingecko.com/api/v3/coins/{select}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': selectInterval,
        'interval': 'hourly'
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if(response.status_code != 200):
        st.write('Error while gettinf data for CoinGecko API :(')
    else:
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        max_price = df['price'].max()
        min_price = df['price'].min()
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

        # st.line_chart(df,x='datetime',y='price')
        myScale = alt.Scale(domainMax=max_price, domainMin=min_price)
        lineChart = alt.Chart(df).mark_line(clip=True).encode(
        x='datetime',
        y=alt.Y('price',scale=myScale)
        ).interactive()
        st.altair_chart(lineChart,use_container_width=True)
            
        
@st.cache(ttl=24*60*60)
def displayDf(responseReddit, df_post_reddit ):
    for post in responseReddit.json()['data']['children']: # iterate over the posts to make a df to show
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
        }, ignore_index=True)
    return df_post_reddit # show the dataframe with streamlit      


def rating(string):
    text_blob_obj = TextBlob(string)
    sentiment_score = text_blob_obj.sentiment.polarity
    sentiment_score_0_to_100 = (sentiment_score + 1) * 50
    return sentiment_score_0_to_100;


