FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py
# No se requiren en Google Cloud
# COPY .env .env
# COPY test_app.py test_app.py

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
