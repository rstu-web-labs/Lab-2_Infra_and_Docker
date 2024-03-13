FROM python:3.12-alpine

WORKDIR WebDocker

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app app