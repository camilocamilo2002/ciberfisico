from flask import Flask, jsonify, request
import time
import threading
import math

app = Flask(__name__)

nivel_agua = 50.0
cloro_ppm = 1.50
bomba_activa = False
ultimo_tiempo = time.time()

# Tasas para ciclo de 30-60 segundos (Delta Time)
TASA_LLENADO = 2.5   # % por segundo (caudal de entrada continuo)
TASA_VACIADO = 5.0   # % por segundo (extracción cuando la bomba se activa)

def bucle_fisico():
    global nivel_agua, cloro_ppm, bomba_activa, ultimo_tiempo
    tiempo_inicio = time.time()
    while True:
        ahora = time.time()
        dt = ahora - ultimo_tiempo
        ultimo_tiempo = ahora

        # Dinámica de nivel basada en Delta Time
        if bomba_activa:
            nivel_agua -= (TASA_VACIADO - TASA_LLENADO) * dt
        else:
            nivel_agua += TASA_LLENADO * dt

        nivel_agua = max(0.0, min(100.0, nivel_agua))

        # Dinámica química de cloro (oscila entre 0.10 y 4.30 ppm para evidenciar alarmas)
        t_transcurrido = ahora - tiempo_inicio
        cloro_ppm = round(2.20 + 2.10 * math.sin(t_transcurrido / 15.0), 2)

        time.sleep(0.5)

@app.route('/api/nivel', methods=['GET'])
def obtener_estado():
    return jsonify({
        "nivel": int(round(nivel_agua)),
        "cloro": cloro_ppm,
        "bomba": 1 if bomba_activa else 0
    }), 200

@app.route('/api/bomba', methods=['POST'])
def controlar_bomba():
    global bomba_activa
    datos = request.get_json(force=True)
    bomba_activa = bool(datos.get("estado", 0))
    return jsonify({"status": "ok", "bomba": int(bomba_activa)}), 200

if __name__ == '__main__':
    hilo = threading.Thread(target=bucle_fisico, daemon=True)
    hilo.start()
    app.run(host='0.0.0.0', port=5000)
