import time
import requests
from pymodbus.client import ModbusTcpClient

API_URL = "http://192.168.10.11:5000/api/bomba"
PLC_IP = "192.168.10.10"

client = ModbusTcpClient(PLC_IP, port=502)
estado_anterior = -1

while True:
    try:
        if client.connect():
            # 1. Leer estado ordenado por el PLC (Registro 1)
            result = client.read_holding_registers(1, 1)
            if not result.isError():
                estado_actual = result.registers[0]
                # 2. Si hay cambio, enviar a API REST del Estanque
                if estado_actual != estado_anterior:
                    payload = {"estado": estado_actual}
                    requests.post(API_URL, json=payload, timeout=2)
                    print(f"Actuador: Bomba cambiada a estado {estado_actual}")
                    estado_anterior = estado_actual
        else:
            print(f"Actuador: Esperando conexión con PLC en {PLC_IP}:502...")
    except Exception as e:
        print(f"Error en actuador: {e}")
    time.sleep(1)
