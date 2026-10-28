import time
import json
from pymodbus.client import ModbusTcpClient
import paho.mqtt.client as mqtt

PLC_IP = "192.168.10.10"
BROKER_IP = "192.168.20.20"

modbus_client = ModbusTcpClient(PLC_IP, port=502)
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "gateway_borde")

conectado_mqtt = False
while not conectado_mqtt:
    try:
        mqtt_client.connect(BROKER_IP, 1883, 60)
        mqtt_client.loop_start()
        conectado_mqtt = True
        print(f"Gateway conectado exitosamente al Broker MQTT ({BROKER_IP})")
    except Exception as e:
        print(f"Esperando al Broker MQTT ({BROKER_IP})... {e}")
        time.sleep(2)

while True:
    try:
        if modbus_client.connect():
            # Leer HR0 (Nivel), HR1 (Bomba), HR2 (Cloro * 100)
            rr = modbus_client.read_holding_registers(0, count=3, slave=1)
            if not rr.isError():
                nivel = rr.registers[0]
                bomba = rr.registers[1]
                cloro = round(rr.registers[2] / 100.0, 2)

                payload = json.dumps({
                    "nivel": nivel,
                    "bomba": bomba,
                    "cloro": cloro,
                    "timestamp": time.time()
                })
                mqtt_client.publish("telemetria/planta", payload)
                print(f"Gateway -> MQTT: {payload}")
        else:
            print(f"Gateway: No se pudo conectar al PLC ({PLC_IP}:502)")
    except Exception as e:
        print(f"Error en Gateway: {e}")
    time.sleep(2)
