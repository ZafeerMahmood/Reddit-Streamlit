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

