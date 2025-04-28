from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_utils import conectar_db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre, u.email, u.password, u.rol
            FROM usuarios u
            WHERE email = %s
            LIMIT 1
        """, (email,))
        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(usuario[3], password):
            user = User(
                id=usuario[0],
                nombre=usuario[1],
                email=usuario[2],
                password=usuario[3],
                rol=usuario[4]
            )
            
            login_user(user)
            
            # Redirección de rol
            if user.rol == 'admin':
                return redirect(url_for('admin_panel'))
            
            else:
                return redirect(url_for('index'))
            
            
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.register'))

        conexion = conectar_db()
        cursor = conexion.cursor()

        # Verificar si el email ya existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conexion.close()
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))

        # Insertar si no existe
        password_hashed = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellidos, email, password, rol) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellidos, email, password_hashed, 'usuario')
        )
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

@auth.route('/editar_usuario_modal/<int:user_id>', methods=['POST'])
@login_required
def editar_usuario_modal(user_id):
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    email = request.form['email']

    conexion = conectar_db()
    cursor = conexion.cursor()

    # Validar email duplicado
    cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email, user_id))
    if cursor.fetchone():
        conexion.close()
        flash('Este correo electrónico ya está en uso.', 'danger')
        return redirect(url_for('admin_panel'))

    cursor.execute("""
        UPDATE usuarios
        SET nombre = %s, apellidos = %s, email = %s
        WHERE id = %s
    """, (nombre, apellidos, email, user_id))
    conexion.commit()
    conexion.close()

    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('admin_panel'))

# Creación de usuario desde el panel de administración
@auth.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash('Las contraseñas no coinciden.', 'danger')
        return redirect(url_for('admin_panel'))

    conexion = conectar_db()
    cursor = conexion.cursor()

    # Verificar si el email ya existe
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        conexion.close()
        flash('El correo electrónico ya está registrado.', 'danger')
        return redirect(url_for('admin_panel'))

    password_hashed = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO usuarios (nombre, apellidos, email, password, rol) VALUES (%s, %s, %s, %s, %s)",
        (nombre, apellidos, email, password_hashed, 'usuario')
    )
    conexion.commit()
    conexion.close()

    flash('Usuario creado correctamente.', 'success')
    return redirect(url_for('admin_panel'))

