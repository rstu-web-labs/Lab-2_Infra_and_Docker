FROM python:3.11

WORKDIR WD

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app app
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]


