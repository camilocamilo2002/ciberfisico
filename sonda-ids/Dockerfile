FROM python:3.9-slim
WORKDIR /app
# Scapy requiere tcpdump en el sistema base para capturar paquetes
RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir scapy
COPY ids.py /app/ids.py
CMD ["python3", "-u", "/app/ids.py"]
