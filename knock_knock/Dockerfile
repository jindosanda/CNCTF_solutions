FROM python:3.11-slim
WORKDIR /app
RUN pip install python-dotenv
COPY knock_sum_server.py .
COPY .env .
EXPOSE 31777
CMD ["python", "knock_sum_server.py"]



