FROM python:3.9-slim
WORKDIR /app

# Instalar dependencias
RUN pip install --no-cache-dir paho-mqtt requests urllib3

# Copiar el script definitivo dentro de la imagen
COPY puente.py /app/puente.py

# Comando de ejecución automática al encender el contenedor
CMD ["python3", "-u", "/app/puente.py"]
