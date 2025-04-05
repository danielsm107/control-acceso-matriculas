from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from routes.auth import auth as auth_blueprint
from utils.db_utils import conectar_db, User
from flask_login import LoginManager
import time
import pytz

app = Flask(__name__)
socketio = SocketIO(app)
app.register_blueprint(auth_blueprint, url_prefix="/auth")

# Configuracion de login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



# Ruta principal (index)
@app.route("/")
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
    datos = request.json
    matricula = datos.get("matricula")

    if not matricula:
        return jsonify({"error": "No se ha proporcionado ninguna matricula"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Verificar si la matricula esta en la base de datos
    cursor.execute("SELECT autorizado FROM matriculas WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:  # Si no existe, devolvemos error y no insertamos nada
        conexion.close()
        return jsonify({"error": "Matricula no registrada"}), 404

    autorizado = resultado[0]  # Si la matricula existe, obtenemos su estado

    # Registrar el acceso en la base de datos
    cursor.execute("INSERT INTO registros_accesos (matricula, autorizado) VALUES (%s, %s)", (matricula, autorizado))
    conexion.commit()

    # Emitir evento WebSocket
    socketio.emit("nuevo_acceso", {
    	"matricula": matricula,
    	"autorizado": autorizado,
    	"fecha": datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M:%S")
    })

    conexion.close()
    return jsonify({"acceso": autorizado})


@app.route("/historial")
def historial():
    filtro = request.args.get("filtro", "todos")  # por defecto "todos"
    conexion = conectar_db()
    cursor = conexion.cursor()

    if filtro == "hoy":
        cursor.execute("""
            SELECT matricula, fecha, autorizado
            FROM registros_accesos
            WHERE DATE(fecha) = CURDATE()
            ORDER BY fecha DESC
        """)
    elif filtro == "ultimos7":
        cursor.execute("""
            SELECT matricula, fecha, autorizado
            FROM registros_accesos
            WHERE fecha >= NOW() - INTERVAL 7 DAY
            ORDER BY fecha DESC
        """)
    else:
        cursor.execute("""
            SELECT matricula, fecha, autorizado
            FROM registros_accesos
            ORDER BY fecha DESC
            LIMIT 50
	 """)
    historial = cursor.fetchall()
    conexion.close()
    return render_template("historial.html", historial=historial, filtro=filtro)

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


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)

