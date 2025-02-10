FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY .env .env

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
