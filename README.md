# Dashboard with python streamlit

uses reddit api for python scripts to get new/hots post show it in a table
make bigram and trigram.

then gets cryptocurrency data from a api of the last 24hours
and display a graph of price to hours.

finally does sentiment analysis on the text of reddit's post.

sensitive information is stored in the .env file not uploaded.

## dependencies

```text
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
```

## env

```sh
secret_key = '<YOUR_KEY>'
client_id = '<YOUR_CLIENT_ID>'
password='<PASSWORD>'
nameForReddit="<USERNAME>"
```



## steps to run

 . reddit api secret key python script client id Lookup example.env make your own .env file replace the given values

   ```cmd
      git clone https://github.com/ZafeerMahmood/Dashboard-python-.git
      cd pythonDashboard/src
      py getData.py
      streamlit run app.py
   ```

## docker

   file

   ```docker
    FROM python:3.11-slim
    
    WORKDIR /app
    
    COPY re.txt ./re.txt
    
    RUN pip install -r re.txt
    
    RUN python -m nltk.downloader punkt
    RUN python -m nltk.downloader stopwords
    RUN python -m nltk.downloader wordnet
    
    EXPOSE 8501
    
    COPY . .
    
    CMD streamlit run app.py
   ```

   to run

   ```cmd
   docker build -f Dockerfile -t app:latest .
   docker run -p 8501:8501 app:latest
   ```


## Screen Shots

![Alt text](https://raw.githubusercontent.com/ZafeerMahmood/Dashboard-python-/main/screenshots/sc1.png?raw=true "1")
![Alt text](https://raw.githubusercontent.com/ZafeerMahmood/Dashboard-python-/main/screenshots/sc2.png?raw=true "2")
