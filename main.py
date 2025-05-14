from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ruta de verificación para Render
@app.route("/", methods=["GET"])
def home():
    return "API activa. Usa POST en /banxico-fix con {fecha: YYYY-MM-DD}"

@app.route("/banxico-fix", methods=["POST"])
def get_fix():
    data = request.get_json()
    fecha = data.get("fecha")  # formato YYYY-MM-DD

    if not fecha:
        return jsonify({"error": "Falta el parámetro 'fecha'"}), 400

    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/{fecha}/{fecha}"
    headers = {
        "Bmx-Token": "33b2de662c9a7b961c3e62b39d2360b31bfca4221d2e86d7769e6c6fd2af2731"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error consultando Banxico"}), 500

    try:
        dato = response.json()["bmx"]["series"][0]["datos"][0]["dato"]
        return jsonify({"tipo_cambio_fix": dato})
    except (KeyError, IndexError):
        return jsonify({"tipo_cambio_fix": "N/E"})
