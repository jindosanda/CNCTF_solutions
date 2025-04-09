FROM python:3.11-slim
WORKDIR /app
RUN pip install dnslib
COPY dns_flag_server.py .
EXPOSE 31100/udp
CMD ["python", "dns_flag_server.py"]
