# utils/db_utils.py
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
    def __init__(self, id, nombre, email, password, matricula=None, rol='usuario', foto=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.matricula = matricula
        self.rol = rol
        self.foto = foto

# Cargar usuario para login
def load_user(user_id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, email, password, rol, foto FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    conexion.close()
    if usuario:
        return User(
            id=usuario[0],
            nombre=usuario[1],
            email=usuario[2],
            password=usuario[3],
            rol=usuario[4],
            foto=usuario[5]
        )
    return None
