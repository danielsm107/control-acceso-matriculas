from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="flask_user",
        password="flask_user",
        database="control_acceso"
    )


# Ruta principal (index)
@app.route("/")
def index():
    return render_template("index.html")


# Endpoint para recibir matrículas desde la Raspberry Pi
@app.route("/recibir_matricula", methods=["POST"])
def recibir_matricula():
    data = request.json
    matricula = data.get("matricula")

    if not matricula:
        return jsonify({"error": "No se ha proporcionado ninguna matricula"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Verificar si la matrícula está en la base de datos
    cursor.execute("SELECT autorizado FROM matriculas WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()

    if resultado is None:  # Si no existe, devolvemos error y no insertamos nada
        conexion.close()
        return jsonify({"error": "Matricula no registrada"}), 404

    autorizado = resultado[0]  # Si la matrícula existe, obtenemos su estado

    # Registrar el acceso en la base de datos
    cursor.execute("INSERT INTO registros_accesos (matricula, autorizado) VALUES (%s, %s)", (matricula, autorizado))
    conexion.commit()
    
    conexion.close()

    return jsonify({"acceso": autorizado})

@app.route("/historial")
def historial():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT matricula, fecha, autorizado FROM registros_accesos ORDER BY fecha DESC")
    historial = cursor.fetchall()
    conexion.close()
    return render_template("historial.html", historial=historial)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

