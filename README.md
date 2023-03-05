# Dasboard with python stramlit

uses reddit api for python scripts to get new/hots post show it in a table
make bigram and trigram.

then gets cryptocurrency data from a api of the last 24hours
and display a graph of price to hours.

finally does sentiment analaysis on the text of reddits post.

sensitive information is sroted in the .env file not uploaded.

# libaries required to run


Python                       3.11.1
pandas                       1.5.3
requests                     2.28.2
streamlit                    1.17.0
dotenv
altair                       4.2.2
transformers                 4.26.1
tensorflow                   2.12.0rc0
unicodedata
nltk                         3.8.1
nltk.corpus
nltk with 'punkt' 'stopwords' 
huggingface-hub              0.12.1
pip                          23.0.1

# steps to run

0. # reddit api secret key python script client id Lookup example.env 
   make your own .env file replace the given values

1. # py getData.py

2. # streamlit run project2.py

# docker info 
   to run 
   docker build -f Dockerfile -t app:latest .
   docker run -p 8501:8501 app:latest


