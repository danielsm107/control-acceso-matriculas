from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, conectar_db

auth = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, email, password FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(usuario[3], password):
            login_user(User(*usuario))
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        conexion.commit()
        conexion.close()

        flash('Cuenta creada correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
