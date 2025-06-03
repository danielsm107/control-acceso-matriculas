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

    # Obtener estado y usuario_id
    cursor.execute("SELECT estado, usuario_id FROM matriculas WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        conexion.close()
        return jsonify({"error": "Matrícula no registrada"}), 404

    estado, usuario_id = resultado
    nombre_imagen = None

    if imagen:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_imagen = f"{matricula}_{timestamp}.jpg"
        ruta_imagen = os.path.join("static/imagenes", nombre_imagen)
        imagen.save(ruta_imagen)

    # Verificar última matrícula para evitar duplicado inmediato
    cursor.execute("""
        SELECT matricula FROM registros_accesos
        ORDER BY fecha DESC LIMIT 1
    """)
    ultimo_registro = cursor.fetchone()

    if ultimo_registro and ultimo_registro[0] == matricula:
        conexion.close()
        return jsonify({"mensaje": "Matrícula ya registrada como última. Ignorada."}), 200

    # Fecha formateada para zona horaria española
    fecha_actual = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M:%S")

    # Insertar registro de acceso
    cursor.execute("""
        INSERT INTO registros_accesos (matricula, estado, imagen, fecha, usuario_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (matricula, estado, nombre_imagen, fecha_actual, usuario_id))
    conexion.commit()

    # Obtener info del usuario para el canal admin
    cursor.execute("SELECT nombre, apellidos, email FROM usuarios WHERE id = %s", (usuario_id,))
    user_data = cursor.fetchone()
    nombre, apellidos, email = user_data if user_data else ("", "", "")

    # Emitir a usuario individual
    socketio.emit(f"nuevo_acceso_{usuario_id}", {
        "matricula": matricula,
        "estado": estado,
        "fecha": fecha_actual,
        "imagen": nombre_imagen,
        "usuario_id": usuario_id
    })

    # Emitir a canal de admin con datos de usuario
    socketio.emit("nuevo_acceso_admin", {
        "matricula": matricula,
        "estado": estado,
        "fecha": fecha_actual,
        "imagen": nombre_imagen,
        "usuario_id": usuario_id,
        "nombre": nombre,
        "apellidos": apellidos,
        "email": email
    })

    conexion.close()
    return jsonify({"acceso": estado, "imagen": nombre_imagen})


