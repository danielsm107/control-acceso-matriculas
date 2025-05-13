from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_socketio import SocketIO, emit
# from datetime import datetime
from routes.auth import auth as auth_blueprint
from utils.db_utils import conectar_db, User, load_user
from routes import auth, main, admin, matriculas, api
from flask_login import LoginManager, current_user, login_required
# import os
# import time
# import pytz
# import re

app = Flask(__name__)
app.secret_key = "clave_segura"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = None
login_manager.init_app(app)
login_manager.user_loader(load_user)

# Registrar Blueprints
app.register_blueprint(auth.auth)
app.register_blueprint(main.main)
app.register_blueprint(admin.admin)
app.register_blueprint(matriculas.matriculas)
app.register_blueprint(api.api)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)


# app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # Limitar a 10 MB
# app.secret_key = "clave_segura"
# socketio = SocketIO(app)
# app.register_blueprint(auth_blueprint)

# # Configuracion de login
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# # Eliminar mensaje flash de inicio de sesión
# login_manager.login_message = None


# @app.route("/")
# @login_required
# def index():
#     conexion = conectar_db()
#     cursor = conexion.cursor()

#     # Traer todas las matrículas del usuario
#     cursor.execute("SELECT matricula, estado FROM matriculas WHERE usuario_id = %s", (current_user.id,))
#     matriculas = cursor.fetchall()

#     # Contar entradas por día para ese usuario
#     cursor.execute("""
#         SELECT DATE(fecha_registro), COUNT(*) 
#         FROM matriculas 
#         WHERE usuario_id = %s
#         GROUP BY DATE(fecha_registro)
#         ORDER BY DATE(fecha_registro)
#     """, (current_user.id,))
#     resultados = cursor.fetchall()

#     fechas = [fila[0].strftime("%d/%m") for fila in resultados]
#     cantidades = [fila[1] for fila in resultados]

#     conexion.close()

#     return render_template("index.html",
#                            matriculas=matriculas,
#                            fechas=fechas,
#                            cantidades=cantidades)


# # Error 413: Para cuando la imagen es demasiado grande
# @app.errorhandler(413)
# def too_large(e):
#     flash("La imagen es demasiado grande. El límite es de 10 MB.", "danger")
#     return redirect(url_for("index"))

# # Redirrecionar según rol
# def _redirect_matriculas():
#     if current_user.rol == 'admin':
#         return redirect(url_for('auth.matriculas_admin'))
#     else:
#         return redirect(url_for('mis_matriculas'))



# @login_manager.user_loader
# def load_user(user_id):
#     conexion = conectar_db()
#     cursor = conexion.cursor()
#     cursor.execute("SELECT id, nombre, email, password, rol, foto FROM usuarios WHERE id = %s", (user_id,))
#     usuario = cursor.fetchone()
#     conexion.close()
#     if usuario:
#         return User(
#             id=usuario[0],
#             nombre=usuario[1],
#             email=usuario[2],
#             password=usuario[3],
#             rol=usuario[4],
#             foto=usuario[5]
#         )
#     return None


# # Endpoint para recibir matriculas desde la raspberry pi
# @app.route("/recibir_matricula", methods=["POST"])
# def recibir_matricula():
#     if request.content_type.startswith("multipart/form-data"):
#         matricula = request.form.get("matricula")
#         imagen = request.files.get("imagen")
#     else:
#         datos = request.get_json()
#         matricula = datos.get("matricula")
#         imagen = None

#     if not matricula:
#         return jsonify({"error": "No se ha proporcionado ninguna matrícula"}), 400

#     conexion = conectar_db()
#     cursor = conexion.cursor()

#     cursor.execute("SELECT estado FROM matriculas WHERE matricula = %s", (matricula,))
#     resultado = cursor.fetchone()

#     if resultado is None:
#         conexion.close()
#         return jsonify({"error": "Matrícula no registrada"}), 404

#     estado = resultado[0]

#     # Guardar imagen si se recibió
#     nombre_imagen = None
#     if imagen:
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         nombre_imagen = f"{matricula}_{timestamp}.jpg"
#         ruta_imagen = os.path.join("static/imagenes", nombre_imagen)
#         imagen.save(ruta_imagen)

#     # Guardar la fecha
#     fecha_actual = datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d %H:%M:%S")

#     # Registrar acceso
#     cursor.execute(
#         "INSERT INTO registros_accesos (matricula, estado, imagen, fecha) VALUES (%s, %s, %s, %s)",
#         (matricula, estado, nombre_imagen, fecha_actual)
#     )
#     conexion.commit()

#     socketio.emit("nuevo_acceso", {
#         "matricula": matricula,
#         "estado": estado,
#         "fecha": fecha_actual,
#         "imagen": nombre_imagen
#     })

#     conexion.close()
#     return jsonify({"acceso": estado, "imagen": nombre_imagen})
