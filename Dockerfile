FROM python:3.7-slim
WORKDIR /app
COPY app /app
ADD requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md

CMD ["source", "run_server.sh"]
