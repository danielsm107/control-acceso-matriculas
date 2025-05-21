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

    # Solo autorizadas o denegadas
    cursor.execute("""
        SELECT matricula, estado
        FROM matriculas
        WHERE usuario_id = %s AND estado IN ('autorizada', 'denegada')
    """, (current_user.id,))
    matriculas = cursor.fetchall()

    # Solo las pendientes
    cursor.execute("SELECT matricula FROM matriculas WHERE usuario_id = %s AND estado = 'pendiente'", (current_user.id,))
    pendientes = [fila[0] for fila in cursor.fetchall()]

    # Gráfico de accesos reales
    cursor.execute("""
        SELECT DATE(fecha), COUNT(*) 
        FROM registros_accesos 
        WHERE usuario_id = %s
        GROUP BY DATE(fecha)
        ORDER BY DATE(fecha)
    """, (current_user.id,))
    resultados = cursor.fetchall()

    fechas = [fila[0].strftime("%d/%m") for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    conexion.close()

    return render_template("index.html", matriculas=matriculas, pendientes=pendientes, fechas=fechas, cantidades=cantidades)





@main.route("/historial")
@login_required
def historial():
    filtro = request.args.get("filtro", "todos")
    conexion = conectar_db()
    cursor = conexion.cursor()

    if current_user.rol == "admin":
        query = """
            SELECT ra.matricula, ra.fecha, ra.estado, ra.imagen, u.nombre, u.apellidos, u.email
            FROM registros_accesos ra
            LEFT JOIN usuarios u ON ra.usuario_id = u.id
        """
        if filtro == "hoy":
            query += " WHERE DATE(ra.fecha) = CURDATE()"
        elif filtro == "ultimos7":
            query += " WHERE ra.fecha >= NOW() - INTERVAL 7 DAY"
    else:
        query = """
            SELECT matricula, fecha, estado, imagen
            FROM registros_accesos
            WHERE usuario_id = %s
        """
        params = [current_user.id]
        if filtro == "hoy":
            query += " AND DATE(fecha) = CURDATE()"
        elif filtro == "ultimos7":
            query += " AND fecha >= NOW() - INTERVAL 7 DAY"
        query += " ORDER BY fecha DESC LIMIT 50"
        cursor.execute(query, tuple(params))

        historial = cursor.fetchall()
        conexion.close()

        historial_format = [(m, f.strftime("%d/%m/%Y %H:%M"), e, i) for m, f, e, i in historial]
        return render_template("historial.html", historial=historial_format, filtro=filtro)

    # Solo para admin
    query += " ORDER BY ra.fecha DESC LIMIT 50"
    cursor.execute(query)
    historial = cursor.fetchall()
    conexion.close()

    historial_format = [
        (m, f.strftime("%d/%m/%Y %H:%M"), e, i, n, a, em)
        for m, f, e, i, n, a, em in historial
    ]
    return render_template("historial.html", historial=historial_format, filtro=filtro)



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