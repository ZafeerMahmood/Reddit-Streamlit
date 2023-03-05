
import streamlit as st
from components import chart,makeBarChartBigrams,makeBarChartTrigrams
import pandas as pd

st.set_page_config(layout='wide')
st.title('Dashboard for Reddit')

col1, col2, col3 = st.columns([0.4,2.5,0.4])
subreddit = "wallstreetbets" 


with st.container():
    with col1:
        st.markdown('#')
       # subreddit = st.text_input('Enter subreddit name', subreddit)
        type =st.selectbox('select type?', ('hot', 'new',))
        limit =  st.selectbox(
            'select Limit?',
            ('50','100'))


 
redditPost=pd.read_csv(f'data_{type}.csv')
redditPost.drop('Unnamed: 0',axis=1,inplace=True)


with st.container():
    with col2:
        st.write(f'{type} posts from wallstreetbets')
        st.dataframe(redditPost,use_container_width=True)

mean=redditPost['Sentiment_score'].mean()
mean=round(mean,4)
avg=redditPost['Sentiment'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'

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
    makeBarChartBigrams(redditPost)
with c3:
    makeBarChartTrigrams(redditPost)






