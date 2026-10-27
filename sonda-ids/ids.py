import sys
from scapy.all import sniff, IP, TCP, Raw

print("Sonda IDS Iniciada. Análisis DPI de tramas Modbus en modo promiscuo...")

LISTA_BLANCA_ESCRITURA = ["192.168.10.10", "192.168.10.30"] # Solo PLC y HMI local podrían escribir
FUNCIONES_ESCRITURA = [5, 6, 15, 16] # Códigos Modbus para forzar bobinas o escribir registros

def inspeccion_profunda_modbus(paquete):
    # Verificar si es TCP dirigido al puerto Modbus y si contiene datos crudos (Payload)
    if paquete.haslayer(IP) and paquete.haslayer(TCP) and paquete.haslayer(Raw):
        ip_origen = paquete[IP].src
        puerto_destino = paquete[TCP].dport

        if puerto_destino == 502:
            payload = paquete[Raw].load
            # El encabezado MBAP de Modbus TCP tiene 7 bytes. El byte 8 (índice 7) es el Código de Función.
            if len(payload) >= 8:
                codigo_funcion = payload[7]
                
                # Si el código detectado es de escritura y la IP no está autorizada
                if codigo_funcion in FUNCIONES_ESCRITURA and ip_origen not in LISTA_BLANCA_ESCRITURA:
                    print(f"[CRÍTICO] Comando de ESCRITURA no autorizado interceptado:")
                    print(f" -> IP Atacante: {ip_origen}")
                    print(f" -> Código de Función Modbus: {codigo_funcion}")
                    print(f" -> Acción bloqueada/alertada por política IDS.\n")

sniff(iface="eth0", prn=inspeccion_profunda_modbus, store=0)
