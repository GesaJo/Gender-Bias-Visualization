FROM python:3.7-slim
WORKDIR /app
COPY app /app
ADD requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt averaged_perceptron_tagger wordnet
RUN python -m spacy download en_core_web_md


ENTRYPOINT ["python"]

CMD ["application.py"]
