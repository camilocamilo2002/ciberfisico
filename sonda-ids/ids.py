import sys
from scapy.all import sniff, IP, TCP

print("Sonda IDS Iniciada. Escuchando tráfico Modbus en modo promiscuo...")

# IPs permitidas (Sensor, Actuador, Gateway, Panel HMI)
LISTA_BLANCA = ["192.168.10.12", "192.168.10.13", "192.168.10.21", "192.168.10.30"]
IP_PLC = "192.168.10.10"

def detectar_intrusion(paquete):
    if paquete.haslayer(IP) and paquete.haslayer(TCP):
        ip_origen = paquete[IP].src
        ip_destino = paquete[IP].dst
        puerto_destino = paquete[TCP].dport

        # Si el tráfico va hacia el PLC en el puerto Modbus (502)
        if ip_destino == IP_PLC and puerto_destino == 502:
            if ip_origen not in LISTA_BLANCA:
                print(f"[*] ALERTA DE SEGURIDAD: Conexión Modbus no autorizada desde IP {ip_origen}")

# Escuchar en la interfaz eth0 sin filtros estrictos de BPF para evitar bloqueos del sistema operativo
sniff(iface="eth0", prn=detectar_intrusion, store=0)
