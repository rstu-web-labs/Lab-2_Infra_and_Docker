FROM python:alpine
WORKDIR /
COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ../app ./app
