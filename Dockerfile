# syntax=docker/dockerfile:1

FROM python:3.10.14-slim
WORKDIR /app
COPY . .
RUN apt-get -y update

RUN apt-get install -y sqlite3 libsqlite3-dev

RUN mkdir -p /app/db && sqlite3 /app/db/ss.db ""

RUN pip install --upgrade pip
RUN pip install peewee
CMD ["python3", "-u", "./app/app.py"]