from scapy.all import sniff, IP, TCP
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - ALERTA IDS: %(message)s')

IPS_AUTORIZADAS = ["192.168.10.10", "192.168.10.12", "192.168.10.13", "192.168.10.21", "192.168.10.30"]

def analizar_paquete(paquete):
    if paquete.haslayer(TCP) and paquete.haslayer(IP):
        if paquete[TCP].dport == 502 or paquete[TCP].sport == 502:
            ip_origen = paquete[IP].src
            if ip_origen not in IPS_AUTORIZADAS:
                logging.info(f"Tráfico Modbus NO AUTORIZADO detectado desde IP: {ip_origen}")
            else:
                print(f"[OK] Tráfico Modbus legítimo inspeccionado: {ip_origen} -> {paquete[IP].dst}")

print("Sonda IDS Iniciada. Escuchando tráfico TCP/502 en modo promiscuo...")
sniff(filter="tcp port 502", prn=analizar_paquete, store=0)
