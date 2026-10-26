FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir requests pymodbus
COPY sensor.py /app/sensor.py
CMD ["python3", "-u", "/app/sensor.py"]
