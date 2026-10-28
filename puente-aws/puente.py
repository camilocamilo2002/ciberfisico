import paho.mqtt.client as mqtt
import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BROKER_IP = "192.168.20.20"
aws_ip = os.environ.get("AWS_IP", "127.0.0.1")
AWS_EC2_URL = f"https://{aws_ip}:1880/api/telemetria"

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Puente AWS: Dato recibido de MQTT: {payload}")
    try:
        headers = {'Content-Type': 'application/json'}
        requests.post(AWS_EC2_URL, data=payload, headers=headers, verify=False, timeout=5)
    except Exception as e:
        print(f"Error de conexión con AWS: {e}")

# Instanciación con soporte para paho-mqtt v2.0.0+
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "puente_aws")
client.on_message = on_message
client.connect(BROKER_IP, 1883, 60)
client.subscribe("telemetria/planta")

print(f"Puente AWS conectado al Broker. Destino Cloud: {AWS_EC2_URL}")
client.loop_forever()
