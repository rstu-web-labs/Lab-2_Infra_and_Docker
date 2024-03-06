FROM python:3.11-alpine

WORKDIR /App

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./app ./app