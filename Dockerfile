FROM python:3.7-slim
WORKDIR /app
ADD requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["source run_server.sh"]
