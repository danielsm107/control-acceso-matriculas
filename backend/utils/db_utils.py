from flask_login import UserMixin
import mysql.connector

# Conexion a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="flask_user",
        password="flask_user",
        database="control_acceso"
    )

class User(UserMixin):
    def __init__(self, id, nombre, email, password, matricula, rol='usuario'):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.matricula = matricula
        self.rol = rol