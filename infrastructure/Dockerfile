FROM python:3.11-alpine3.19

WORKDIR src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app/ ./app/

