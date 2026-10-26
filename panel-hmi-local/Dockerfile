FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir flask pymodbus
COPY app.py /app/app.py
EXPOSE 8080
CMD ["python3", "-u", "/app/app.py"]
