FROM python:3.11-alpine
WORKDIR /proj
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app ./app