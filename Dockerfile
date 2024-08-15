FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app
COPY ./resources /app/resources

RUN apt-get update && apt-get install -y redis-server

EXPOSE 5000

CMD service redis-server start && python3 main.py
