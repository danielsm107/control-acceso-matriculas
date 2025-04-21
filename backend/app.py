from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
from routes.auth import auth as auth_blueprint
from utils.db_utils import conectar_db, User
from flask_login import LoginManager, current_user, login_required
import os
import time
import pytz

app = Flask(__name__)
app.secret_key = "clave_segura"
socketio = SocketIO(app)
app.register_blueprint(auth_blueprint)

# Configuracion de login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



# Ruta principal (index)
@app.route("/")
@login_required
def index():
    return render_template("index.html")



@login_manager.user_loader
def load_user(user_id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, email, password FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    conexion.close()
    if usuario:
        return User(*usuario)
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

    cursor.execute("SELECT autorizado FROM matriculas WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:
        conexion.close()
        return jsonify({"error": "Matrícula no registrada"}), 404

    autorizado = resultado[0]

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
        "INSERT INTO registros_accesos (matricula, autorizado, imagen, fecha) VALUES (%s, %s, %s, %s)",
        (matricula, autorizado, nombre_imagen, fecha_actual)
    )
    conexion.commit()

    socketio.emit("nuevo_acceso", {
        "matricula": matricula,
        "autorizado": autorizado,
        "fecha": fecha_actual,
        "imagen": nombre_imagen
    })

    conexion.close()
    return jsonify({"acceso": autorizado, "imagen": nombre_imagen})

@app.route("/historial")
def historial():
    filtro = request.args.get("filtro", "todos")
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Filtrar historial
    if filtro == "hoy":
        cursor.execute("""
            SELECT matricula, fecha, autorizado, imagen
            FROM registros_accesos
            WHERE DATE(fecha) = CURDATE()
            ORDER BY fecha DESC
        """)
    elif filtro == "ultimos7":
        cursor.execute("""
            SELECT matricula, fecha, autorizado, imagen
            FROM registros_accesos
            WHERE fecha >= NOW() - INTERVAL 7 DAY
            ORDER BY fecha DESC
        """)
    else:
        cursor.execute("""
            SELECT matricula, fecha, autorizado, imagen
            FROM registros_accesos
            ORDER BY fecha DESC
            LIMIT 50
        """)

    historial = cursor.fetchall()
    conexion.close()

    # Formatear fechas
    historial_format = []
    for fila in historial:
        matricula, fecha, autorizado, imagen = fila
        fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
        historial_format.append((matricula, fecha_str, autorizado, imagen))

    return render_template("historial.html", historial=historial_format, filtro=filtro)

@app.route("/api/historial")
def api_historial():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT matricula, fecha, autorizado FROM registros_accesos ORDER BY fecha DESC LIMIT 20")
    historial = cursor.fetchall()
    conexion.close()

    datos = []
    for fila in historial:
        datos.append({
            "matricula": fila[0],
            "fecha": fila[1].strftime("%Y-%m-%d %H:%M:%S"),
            "autorizado": fila[2]
        })

    return jsonify(datos)

# Ruta para solicitar matrícula (formulario)
@app.route('/solicitar_matricula', methods=['GET', 'POST'])
@login_required
def solicitar_matricula():
    if request.method == 'POST':
        matricula = request.form['matricula'].upper()

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO matriculas (matricula, autorizado, usuario_id) VALUES (%s, %s, %s)",
            (matricula, False, current_user.id)
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
    cursor.execute("SELECT matricula, autorizado, id FROM matriculas WHERE usuario_id = %s", (current_user.id,))
    datos = cursor.fetchall()
    conexion.close()

    return render_template('mis_matriculas.html', matriculas=datos)


@app.route('/eliminar_matricula/<int:matricula_id>', methods=['POST'])
@login_required
def eliminar_matricula(matricula_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Eliminar solo si la matrícula es del usuario actual
    cursor.execute("DELETE FROM matriculas WHERE id = %s AND usuario_id = %s AND autorizado = FALSE", (matricula_id, current_user.id))
    
    if cursor.rowcount > 0:
        flash('Matrícula eliminada correctamente.', 'success')
    else:
        flash('No se pudo eliminar la matrícula.', 'danger')

    conexion.commit()
    conexion.close()

    return redirect(url_for('mis_matriculas'))


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)

