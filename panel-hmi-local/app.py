from flask import Flask
from pymodbus.client import ModbusTcpClient

app = Flask(__name__)
PLC_IP = "192.168.10.10"

@app.route('/')
def index():
    client = ModbusTcpClient(PLC_IP, port=502)
    html = "<h1>Panel HMI OT (Nivel 3)</h1>"
    if client.connect():
        rr = client.read_holding_registers(0, 3)
        if not rr.isError():
            nivel = rr.registers[0]
            bomba = rr.registers[1]
            cloro = rr.registers[2] / 100.0
            estado = "ACTIVA" if bomba == 1 else "INACTIVA"
            html += f"<h2>Nivel del Estanque: {nivel}%</h2>"
            html += f"<h2>Estado de Bomba: {estado}</h2>"
            html += f"<h2>Cloro Libre: {cloro:.2f} ppm</h2>"
        client.close()
    else:
        html += "<h2 style='color:red;'>Error de conexión con PLC</h2>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
