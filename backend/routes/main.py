# routes/main.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from utils.db_utils import conectar_db
import pytz
from datetime import datetime
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def index():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT matricula, estado FROM matriculas WHERE usuario_id = %s", (current_user.id,))
    matriculas = cursor.fetchall()

    cursor.execute("""
        SELECT DATE(fecha_registro), COUNT(*) 
        FROM matriculas 
        WHERE usuario_id = %s
        GROUP BY DATE(fecha_registro)
        ORDER BY DATE(fecha_registro)
    """, (current_user.id,))
    resultados = cursor.fetchall()

    fechas = [fila[0].strftime("%d/%m") for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    conexion.close()

    return render_template("index.html", matriculas=matriculas, fechas=fechas, cantidades=cantidades)


@main.route("/historial")
@login_required
def historial():
    filtro = request.args.get("filtro", "todos")
    conexion = conectar_db()
    cursor = conexion.cursor()

    # 1. Consulta del historial
    query = "SELECT matricula, fecha, estado, imagen FROM registros_accesos"
    params = []

    if current_user.rol != "admin":
        query += " WHERE usuario_id = %s"
        params.append(current_user.id)

    if filtro == "hoy":
        query += " AND" if current_user.rol != "admin" else " WHERE"
        query += " DATE(fecha) = CURDATE()"
    elif filtro == "ultimos7":
        query += " AND" if current_user.rol != "admin" else " WHERE"
        query += " fecha >= NOW() - INTERVAL 7 DAY"

    query += " ORDER BY fecha DESC LIMIT 50"

    cursor.execute(query, tuple(params))
    historial = cursor.fetchall()

    historial_format = [
        (matricula, fecha.strftime("%d/%m/%Y %H:%M"), estado, imagen)
        for matricula, fecha, estado, imagen in historial
    ]

    # 2. Consulta de matrículas autorizadas para el modal
    cursor.execute("""
        SELECT matricula FROM matriculas
        WHERE usuario_id = %s AND estado = 'autorizada'
    """, (current_user.id,))
    matriculas_usuario = [fila[0] for fila in cursor.fetchall()]

    conexion.close()

    return render_template("historial.html", historial=historial_format, filtro=filtro, matriculas_usuario=matriculas_usuario)




@main.route("/api/historial")
@login_required
def api_historial():
    conexion = conectar_db()
    cursor = conexion.cursor()

    if current_user.rol == 'admin':
        cursor.execute("SELECT matricula, fecha, estado FROM registros_accesos ORDER BY fecha DESC LIMIT 20")
    else:
        cursor.execute("SELECT matricula, fecha, estado FROM registros_accesos WHERE usuario_id = %s ORDER BY fecha DESC LIMIT 20", (current_user.id,))

    historial = cursor.fetchall()
    conexion.close()

    datos = [{
        "matricula": fila[0],
        "fecha": fila[1].strftime("%Y-%m-%d %H:%M:%S"),
        "estado": fila[2]
    } for fila in historial]

    return jsonify(datos)


@main.route("/subir_foto_perfil", methods=["POST"])
@login_required
def subir_foto_perfil():
    imagen = request.files.get("foto")
    if imagen and imagen.filename != "":
        nombre_archivo = secure_filename(f"user_{current_user.id}.png")
        ruta_carpeta = os.path.join("static", "fotos_perfil")
        os.makedirs(ruta_carpeta, exist_ok=True)
        ruta = os.path.join(ruta_carpeta, nombre_archivo)
        imagen.save(ruta)

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET foto = %s WHERE id = %s", (nombre_archivo, current_user.id))
        conexion.commit()
        conexion.close()

        flash("Tu foto de perfil se ha actualizado.", "success")
    else:
        flash("No se seleccionó ninguna imagen válida.", "danger")

    return redirect(url_for("main.index"))

@main.route("/simular_acceso", methods=["POST"])
@login_required
def simular_acceso():
    from app import socketio
    matricula = request.form.get("matricula")

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT estado FROM matriculas WHERE matricula = %s AND usuario_id = %s", (matricula, current_user.id))
    resultado = cursor.fetchone()

    if not resultado:
        conexion.close()
        flash("Matrícula no autorizada o no pertenece al usuario", "danger")
        return redirect(url_for("main.historial"))

    if resultado[0] != "autorizada":
        conexion.close()
        flash("Solo se pueden simular accesos de matrículas autorizadas.", "warning")
        return redirect(url_for("main.historial"))

    estado = resultado[0]
    fecha_actual = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO registros_accesos (matricula, estado, fecha, usuario_id)
        VALUES (%s, %s, %s, %s)
    """, (matricula, estado, fecha_actual, current_user.id))
    conexion.commit()
    conexion.close()

    socketio.emit("nuevo_acceso", {
        "matricula": matricula,
        "estado": estado,
        "fecha": fecha_actual,
        "imagen": None
    })

    flash(f"Se ha simulado un acceso para {matricula}", "success")
    return redirect(url_for("main.historial"))


