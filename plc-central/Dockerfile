FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir pymodbus
COPY plc.py /app/plc.py
CMD ["python3", "-u", "/app/plc.py"]
