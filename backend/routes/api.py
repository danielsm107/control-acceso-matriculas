# routes/api.py
from flask import Blueprint, request, jsonify
from flask_socketio import emit
from utils.db_utils import conectar_db
from datetime import datetime
import os
import pytz

api = Blueprint('api', __name__)

@api.route("/recibir_matricula", methods=["POST"])
def recibir_matricula():
    from app import socketio

    if request.content_type.startswith("multipart/form-data"):
        matricula = request.form.get("matricula")
        imagen = request.files.get("imagen")
    else:
        datos = request.get_json()
        matricula = datos.get("matricula")
        imagen = None

    if not matricula:
        return jsonify({"error": "No se ha proporcionado ninguna matrícula"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT estado FROM matriculas WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        conexion.close()
        return jsonify({"error": "Matrícula no registrada"}), 404

    estado = resultado[0]
    nombre_imagen = None
    if imagen:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_imagen = f"{matricula}_{timestamp}.jpg"
        ruta_imagen = os.path.join("static/imagenes", nombre_imagen)
        imagen.save(ruta_imagen)

    # Bloque para evitar duplicados consecutivos
    cursor.execute("""
        SELECT matricula FROM registros_accesos
        ORDER BY fecha DESC LIMIT 1
    """)
    ultimo_registro = cursor.fetchone()

    if ultimo_registro and ultimo_registro[0] == matricula:
        conexion.close

