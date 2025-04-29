from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
from routes.auth import auth as auth_blueprint
from utils.db_utils import conectar_db, User
from flask_login import LoginManager, current_user, login_required
import os
import time
import pytz
import re

app = Flask(__name__)
app.secret_key = "clave_segura"
socketio = SocketIO(app)
app.register_blueprint(auth_blueprint)

# Configuracion de login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Eliminar mensaje flash de inicio de sesión
login_manager.login_message = None


# Ruta principal (index)
@app.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)



@login_manager.user_loader
def load_user(user_id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, email, password, rol FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    conexion.close()
    if usuario:
        return User(
            id=usuario[0],
            nombre=usuario[1],
            email=usuario[2],
            password=usuario[3],
            rol=usuario[4]
        )
    return None


# Endpoint para recibir matriculas desde la raspberry pi
@app.route("/recibir_matricula", methods=["POST"])
def recibir_matricula():
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

    # Guardar imagen si se recibió
    nombre_imagen = None
    if imagen:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_imagen = f"{matricula}_{timestamp}.jpg"
        ruta_imagen = os.path.join("static/imagenes", nombre_imagen)
        imagen.save(ruta_imagen)

    # Guardar la fecha
    fecha_actual = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M:%S")

    # Registrar acceso
    cursor.execute(
        "INSERT INTO registros_accesos (matricula, estado, imagen, fecha) VALUES (%s, %s, %s, %s)",
        (matricula, estado, nombre_imagen, fecha_actual)
    )
    conexion.commit()

    socketio.emit("nuevo_acceso", {
        "matricula": matricula,
        "estado": estado,
        "fecha": fecha_actual,
        "imagen": nombre_imagen
    })

    conexion.close()
    return jsonify({"acceso": estado, "imagen": nombre_imagen})

@app.route("/historial")
def historial():
    filtro = request.args.get("filtro", "todos")
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Filtrar historial
    if filtro == "hoy":
        cursor.execute("""
            SELECT matricula, fecha, estado, imagen
            FROM registros_accesos
            WHERE DATE(fecha) = CURDATE()
            ORDER BY fecha DESC
        """)
    elif filtro == "ultimos7":
        cursor.execute("""
            SELECT matricula, fecha, estado, imagen
            FROM registros_accesos
            WHERE fecha >= NOW() - INTERVAL 7 DAY
            ORDER BY fecha DESC
        """)
    else:
        cursor.execute("""
            SELECT matricula, fecha, estado, imagen
            FROM registros_accesos
            ORDER BY fecha DESC
            LIMIT 50
        """)

    historial = cursor.fetchall()
    conexion.close()

    # Formatear fechas
    historial_format = []
    for fila in historial:
        matricula, fecha, estado, imagen = fila
        fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
        historial_format.append((matricula, fecha_str, estado, imagen))

    return render_template("historial.html", historial=historial_format, filtro=filtro)

@app.route("/api/historial")
def api_historial():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT matricula, fecha, estado FROM registros_accesos ORDER BY fecha DESC LIMIT 20")
    historial = cursor.fetchall()
    conexion.close()

    datos = []
    for fila in historial:
        datos.append({
            "matricula": fila[0],
            "fecha": fila[1].strftime("%Y-%m-%d %H:%M:%S"),
            "estado": fila[2]
        })

    return jsonify(datos)

@app.route('/solicitar_matricula', methods=['GET', 'POST'])
@login_required
def solicitar_matricula():
    if request.method == 'POST':
        matricula = request.form['matricula'].upper()

        # Validar formato exacto: 4 dígitos + 3 letras
        if not re.fullmatch(r'\d{4}[A-Z]{3}', matricula):
            flash('Formato de matrícula no válido. Debe ser 4 números seguidos de 3 letras (ej: 1234ABC).', 'danger')
            return redirect(url_for('solicitar_matricula'))

        conexion = conectar_db()
        cursor = conexion.cursor()

        # Primero, comprobar si ya la registró este usuario
        cursor.execute("SELECT COUNT(*) FROM matriculas WHERE matricula = %s AND usuario_id = %s", (matricula, current_user.id))
        existe_para_usuario = cursor.fetchone()[0]

        if existe_para_usuario:
            conexion.close()
            flash('Esa matrícula ya la has registrado tú.', 'danger')
            return redirect(url_for('solicitar_matricula'))

        # Después, comprobar si ya existe con otro usuario
        cursor.execute("SELECT COUNT(*) FROM matriculas WHERE matricula = %s", (matricula,))
        ya_existe_global = cursor.fetchone()[0]

        if ya_existe_global:
            conexion.close()
            flash("Esa matrícula ya ha sido registrada por otro usuario.", "danger")
            return redirect(url_for('solicitar_matricula'))

        # Si pasa las dos validaciones, insertamos
        cursor.execute(
            "INSERT INTO matriculas (matricula, estado, usuario_id) VALUES (%s, %s, %s)",
            (matricula, 'pendiente', current_user.id)
        )
        conexion.commit()
        conexion.close()

        flash('Matrícula solicitada correctamente. Pendiente de aprobación.', 'success')
        return redirect(url_for('mis_matriculas'))

    return render_template('solicitar_matricula.html')


# Ruta para ver matrículas asociadas al usuario
@app.route('/mis_matriculas')
@login_required
def mis_matriculas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT matricula, estado, id FROM matriculas WHERE usuario_id = %s", (current_user.id,))
    datos = cursor.fetchall()
    conexion.close()

    return render_template('mis_matriculas.html', matriculas=datos)


@app.route('/eliminar_matricula/<int:matricula_id>', methods=['POST'])
@login_required
def eliminar_matricula(matricula_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Eliminar solo si la matrícula es del usuario actual
    cursor.execute("DELETE FROM matriculas WHERE id = %s AND usuario_id = %s AND estado = 'denegada'", (matricula_id, current_user.id))
    
    if cursor.rowcount > 0:
        flash('Matrícula eliminada correctamente.', 'success')
    else:
        flash('No se pudo eliminar la matrícula.', 'danger')

    conexion.commit()
    conexion.close()

    return redirect(url_for('mis_matriculas'))

# Ruta para administradores
@app.route("/admin")
@login_required
def admin_panel():
    if current_user.rol != 'admin':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('index'))
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Obtener todos los usuarios
    cursor.execute("SELECT id, nombre, apellidos, email, rol FROM usuarios")
    users = cursor.fetchall()

    # Obtener matrículas pendientes de aprobación
    cursor.execute("""
        SELECT m.id, m.matricula, u.nombre, u.apellidos, u.email, m.estado
        FROM matriculas m
        JOIN usuarios u ON m.usuario_id = u.id
        WHERE m.estado = 'pendiente'
    """)
    pendientes = cursor.fetchall()

    conexion.close()
    return render_template("admin_panel.html", users=users, pendientes=pendientes, user=current_user)

# Rutas para aprobar o rechazar matrículas
@app.route("/admin/aprobar/<int:id>", methods=["POST"])
@login_required
def aprobar_matricula(id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("index"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE matriculas SET estado = 'autorizada' WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula aprobada", "success")
    return redirect(url_for("admin_panel"))

@app.route("/admin/rechazar/<int:id>", methods=["POST"])
@login_required
def rechazar_matricula(id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("index"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM matriculas WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula rechazada", "warning")
    return redirect(url_for("admin_panel"))

# Eliminar usuario
@app.route("/admin/eliminar_usuario/<int:user_id>", methods=["POST"])
@login_required
def eliminar_usuario(user_id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("index"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    conexion.commit()
    conexion.close()

    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for("admin_panel"))

# Cambiar rol de usuario
@app.route("/admin/cambiar_rol/<int:user_id>", methods=["POST"])
@login_required
def cambiar_rol(user_id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("index"))

    nuevo_rol = request.form.get("rol")
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, user_id))
    conexion.commit()
    conexion.close()

    flash("Rol actualizado correctamente", "success")
    return redirect(url_for("admin_panel"))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)

