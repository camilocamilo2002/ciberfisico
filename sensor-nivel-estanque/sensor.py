import time
import requests
from pymodbus.client import ModbusTcpClient

ESTANQUE_URL = "http://192.168.10.11:5000/api/nivel"
PLC_IP = "192.168.10.10"
PLC_PORT = 502

client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

while True:
    try:
        resp = requests.get(ESTANQUE_URL, timeout=3)
        if resp.status_code == 200:
            datos = resp.json()
            nivel = int(datos.get("nivel", 0))
            cloro_float = float(datos.get("cloro", 1.5))
            cloro_escalado = int(round(cloro_float * 100))

            if client.connect():
                # Registro 0: Nivel (%)
                client.write_register(0, nivel)
                # Registro 2: Cloro escalado (ppm * 100)
                client.write_register(2, cloro_escalado)
                print(f"Sensor -> PLC | Nivel: {nivel}% (HR0) | Cloro: {cloro_float:.2f} ppm [HR2={cloro_escalado}]")
            else:
                print(f"Sensor: No se pudo conectar al PLC en {PLC_IP}:{PLC_PORT}")
    except Exception as e:
        print(f"Error en sensor: {e}")
    time.sleep(2)
