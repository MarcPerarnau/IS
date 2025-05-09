FROM python:3.11

WORKDIR /app

COPY backend.py .

RUN pip install flask mysql-connector-python scapy requests

CMD ["python", "backend.py"]
