FROM python:3.11-alpine as builder-base
WORKDIR /app
COPY ./app ./app
COPY requirements.txt ./
RUN apk update && apk add curl
RUN pip install -r requirements.txt