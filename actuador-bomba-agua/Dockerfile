FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir requests pymodbus
COPY actuador.py /app/actuador.py
CMD ["python3", "-u", "/app/actuador.py"]
