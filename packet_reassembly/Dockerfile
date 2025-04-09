FROM python:3.11-slim
WORKDIR /app
COPY .env .
RUN pip install python-dotenv
COPY packet_reassembler_server.py .
EXPOSE 31204
CMD ["python", "packet_reassembler_server.py"]
