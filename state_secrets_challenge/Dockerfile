FROM python:3.10-slim

WORKDIR /app

RUN pip install python-dotenv

COPY state_secrets_server.py .
COPY .env .

CMD ["python", "state_secrets_server.py"]
