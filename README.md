# Emulación Ciberfísica de Planta de Tratamiento de Agua (PTSC08)

Repositorio del proyecto de Evaluación Sumativa 2/3 para la asignatura Sistemas Ciberfísicos. Este proyecto implementa una arquitectura industrial bajo el **Modelo Purdue (ISA-95 / IEC 62443)** utilizando GNS3, Docker y AWS EC2.

## Arquitectura de Red y Segmentación

La topología está segmentada en 4 niveles lógicos, aislando la red OT (Tecnología de Operaciones) de la red IT (Tecnología de la Información):

*   **Nivel 1-2 (Control de Procesos):** `estanque-agua` (Gemelo Digital), `sensor-nivel-estanque`, `actuador-bomba-agua`, y `plc-central`.
*   **Nivel 3 (Operaciones OT):** `gateway-borde`, `broker-mqtt`, `panel-hmi-local` y la `sonda-ids` conectada a un puerto SPAN para auditoría pasiva.
*   **Nivel 3.5 (DMZ Perimetral):** Firewall FortiGate ejecutando políticas de "Denegación Implícita" y NAT.
*   **Nivel 4 (Analítica Cloud):** Servidor Node-RED desplegado en AWS EC2 recibiendo telemetría securizada mediante HTTPS/TLS.

## Estructura de Contenedores y Nomenclatura

El código fuente en Python ha sido desarrollado respetando la nomenclatura en español para variables y comentarios, facilitando la auditoría del proceso físico (nivel, bomba, cloro).

| Contenedor | Descripción Técnica | Dependencias Python |
| :--- | :--- | :--- |
| `plc-central` | Servidor Modbus TCP que aloja los *Holding Registers* de la planta. | `pymodbus` |
| `estanque-agua` | API REST Flask que emula la dinámica física de llenado y dosificación. | `flask` |
| `sensor-nivel-estanque` | Transductor que lee de la API y escribe en el PLC. | `requests`, `pymodbus` |
| `actuador-bomba-agua` | Lazo de control que lee comandos del PLC e impacta el estanque. | `pymodbus`, `requests` |
| `gateway-borde` | Traductor de protocolo Modbus TCP a MQTT (Desacoplamiento). | `pymodbus`, `paho-mqtt` |
| `puente-aws` | Cliente MQTT que exporta la telemetría a Node-RED vía HTTPS/TLS. | `paho-mqtt`, `requests`, `urllib3` |
| `sonda-ids` | Sniffer pasivo con Scapy para detección de tráfico Modbus no autorizado. | `scapy` |
| `panel-hmi-local` | Interfaz web de supervisión operativa (Nivel 3). | `flask`, `pymodbus` |

## Despliegue

Cada módulo cuenta con su respectivo `Dockerfile`. Para reconstruir la infraestructura localmente, ejecute:
```bash
docker compose build
