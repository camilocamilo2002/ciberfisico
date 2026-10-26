from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import threading
import time

# Registro 0: Nivel del estanque (0-100)
# Registro 1: Estado de la bomba (0 o 1)
# Registro 2: Cloro (ppm escalado x100)
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [50, 0] + [0]*98)
)
context = ModbusServerContext(slaves=store, single=True)

def lazo_de_control():
    while True:
        # Leer 3 registros desde la dirección 0: Nivel, Bomba y Cloro
        valores = context[0].getValues(3, 0, count=3)
        nivel = valores[0]
        estado_bomba_actual = valores[1]
        cloro_ppm = valores[2] / 100.0 # Desescalar de entero a decimal

        nuevo_estado = estado_bomba_actual
        if nivel >= 90:
            nuevo_estado = 1 # Iniciar extracción
        elif nivel <= 20:
            nuevo_estado = 0 # Detener extracción
        
        if nuevo_estado != estado_bomba_actual:
            context[0].setValues(3, 1, [nuevo_estado])
            nuevo_estado_str = "ACTIVA" if nuevo_estado == 1 else "INACTIVA"
            print(f"[*] ALERTA PLC: Bomba cambiada a estado {nuevo_estado_str}")
        
        # Imprimir telemetría en consola (Evidencia Módulo 1)
        print(f"PLC Control | Nivel: {nivel}% | Bomba: {nuevo_estado} | Cloro: {cloro_ppm:.2f} ppm")

        time.sleep(0.5)

if __name__ == "__main__":
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'INACAP'
    identity.ModelName = 'PLC-Central-Virtual'
    
    threading.Thread(target=lazo_de_control, daemon=True).start()
    print("Iniciando Servidor Modbus TCP en el puerto 502...")
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))
