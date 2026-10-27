import sys
from scapy.all import sniff, IP, TCP, Raw

print("Sonda IDS Iniciada. Análisis DPI de tramas Modbus en modo promiscuo...")

# Solo el sensor-nivel-estanque (192.168.10.12) tiene autorización legítima para escribir registros en el PLC
LISTA_BLANCA_ESCRITURA = ["192.168.10.12"]
FUNCIONES_ESCRITURA = [5, 6, 15, 16]  # Write Single Coil (5), Write Single Register (6), Multiple Coils (15), Multiple Registers (16)

def inspeccion_profunda_modbus(paquete):
    if paquete.haslayer(IP) and paquete.haslayer(TCP) and paquete.haslayer(Raw):
        ip_origen = paquete[IP].src
        ip_destino = paquete[IP].dst
        puerto_destino = paquete[TCP].dport

        if puerto_destino == 502:
            payload = paquete[Raw].load
            # Encabezado MBAP = 7 bytes (índices 0 a 6). El byte 8 (índice 7) es el Function Code Modbus.
            if len(payload) >= 8:
                codigo_funcion = payload[7]
                if codigo_funcion in FUNCIONES_ESCRITURA and ip_origen not in LISTA_BLANCA_ESCRITURA:
                    print(f"[CRÍTICO] Comando de ESCRITURA no autorizado interceptado:")
                    print(f" -> IP Atacante: {ip_origen} -> Destino PLC: {ip_destino}")
                    print(f" -> Código de Función Modbus: {codigo_funcion}")
                    print(f" -> Acción alertada por política IDS (Violación de Integridad OT).\n")

sniff(iface="eth0", prn=inspeccion_profunda_modbus, store=0)
