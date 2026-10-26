FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir pymodbus paho-mqtt
COPY gateway.py /app/gateway.py
CMD ["python3", "-u", "/app/gateway.py"]
