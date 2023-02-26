import requests
import pandas as pd
import streamlit as st
import altair as alt
import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from transformers import pipeline

#hugging face model can be change to any trained model hosted on huggingface.co/models
specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")


#funtion get crypto data from coingecko API and make a chart with altair and streamlit 
# @parametrs: select - the crypto name, selectInterval - the number of days to show
def chart(select, selectInterval):
    endpoint = f'https://api.coingecko.com/api/v3/coins/{select}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': selectInterval,
        'interval': 'hourly'
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if (response.status_code != 200):
        st.write('Error while gettinf data for CoinGecko API :(')
    else:
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        max_price = df['price'].max()
        min_price = df['price'].min()
        mean_price = df['price'].mean()
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

        # st.line_chart(df,x='datetime',y='price')
        myScale = alt.Scale(domainMax=max_price, domainMin=min_price)
        lineChart = alt.Chart(df).mark_line(clip=True).encode(
            x='datetime',
            y=alt.Y('price', scale=myScale)
        ).interactive()
        st.altair_chart(lineChart,use_container_width=True)
        return [max_price, min_price, mean_price]

# funtion thats makes a dataframe with the posts from reddit
#@parameter responseReddit - the response from the reddit API and an emty dataFrame
#@return df_post_reddit - the dataframe with the posts
@st.cache(ttl=24*60*60)
def displayDf(responseReddit):
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
    return df_post_reddit  # show the dataframe with streamlit



#funtion that cleans the unnerrcessary data from the text eg. stopwords, links, etc.
# @parametrs: text - the text to clean
# @return words - the cleaned text
def basic_clean(text):
    stopwords = nltk.corpus.stopwords.words('english')
    text = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    #words = re.sub('http://\S+|https://\S+', '', text).split()
    return [word for word in words if word not in stopwords]







#used to select the columns to show in the dataframe for cleaning and making the bar charts
columns = ['title', 'selftext' ]

#funtion that cleans the unnerrcessary data from a coulmn in the dataframe eg. stopwords, links, etc.
# makes trigram of list of words
# @parametrs: df - the dataframe to clean
# @return df - the cleaned dataframe
def trigrams(df):
    df = df[df[f'{columns[1]}'].str.contains("NaN") == False]
    words = basic_clean(''.join(str(df[f'{columns[1]}'].tolist())))
    trigrams_series = (pd.Series(nltk.ngrams(words, 3)).value_counts())[:10]
    tg = pd.DataFrame({'trigrams': trigrams_series.index,
                      'counts': trigrams_series.values})
    return tg

#funtion that cleans the unnerrcessary data from a coulmn in the dataframe eg. stopwords, links, etc.
# makes bigram of list of words
# @parametrs: df - the dataframe to clean
# @return df - the cleaned dataframe
def bigrams(df):
    df = df[df[f'{columns[1]}'].str.contains("NaN") == False]
    words = basic_clean(''.join(str(df[f'{columns[1]}'].tolist())))
    bigrams_series = (pd.Series(nltk.ngrams(words, 2)).value_counts())[:10]
    bg = pd.DataFrame({'bigrams': bigrams_series.index,
                      'counts': bigrams_series.values})
    return bg


#funtion that makes the required bar charts bigrams
#@parametrs: df - the dataframe to make the charts from
def makeBarChartBigrams(df):
    bg = bigrams(df)
    bg.sort_values(by='counts', ascending=False, inplace=True)
    bars = alt.Chart(bg,height=500).mark_bar().encode(
        x='counts:Q',
        y=alt.Y("bigrams:N", sort='-x')
    )
    st.altair_chart(bars, use_container_width=True)

#funtion that makes the required bar charts bigrams
#@parametrs: df - the dataframe to make the charts from
def makeBarChartTrigrams(df):
    tg = trigrams(df)
    tg.sort_values(by='counts', ascending=False, inplace=True)
    bars = alt.Chart(tg,height=500).mark_bar().encode(
        x='counts:Q',
        y=alt.Y("trigrams:N", sort='-x')
    )
    st.altair_chart(bars, use_container_width=True)
