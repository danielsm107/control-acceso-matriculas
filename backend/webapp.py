from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="flask_user",
        password="flask_user",  # Cambia esto si tienes contraseña en MySQL
        database="control_acceso"
    )

# Endpoint para recibir matrículas desde la Raspberry Pi
@app.route("/recibir_matricula", methods=["POST"])
def recibir_matricula():
    data = request.json
    matricula = data.get("matricula")

    if not matricula:
        return jsonify({"error": "No se proporcionó matrícula"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT autorizado FROM matriculas WHERE matricula = %s", (matricula,))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        return jsonify({"acceso": resultado[0]})
    else:
        return jsonify({"error": "Matrícula no registrada"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
