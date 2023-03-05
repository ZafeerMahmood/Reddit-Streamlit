FROM python:3.11-slim

ADD re.txt /

RUN pip install -r re.txt

RUN python -m nltk.downloader stopwords

RUN python -m nltk.downloader punkt

RUN python -m nltk.downloader wordnet

ADD  getData.py /

ADD components.py /

ADD project2.py /

ADD .env /

ADD data_hot.csv /

ADD data_new.csv /

RUN python ./components.py

RUN python ./getData.py

EXPOSE 8081

ENTRYPOINT ["streamlit", "run", "project2.py", "--server.port=8081", "--server.address=0.0.0.0"]