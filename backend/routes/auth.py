from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_utils import conectar_db, User
from functools import wraps
import re


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

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
            session['rol'] = user.rol

            if user.rol == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

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
    session.clear()
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

def solo_admin(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'rol' not in session or session['rol'] != 'admin':
            flash("Acceso denegado. Solo el administrador puede ver esta página.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorador

@auth.route('/matriculas_admin')
@login_required
@solo_admin
def matriculas_admin():
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Obtener todas las matrículas y sus datos asociados
    cursor.execute("""
        SELECT m.id, m.matricula, u.nombre, u.apellidos, u.email, m.estado, m.fecha_registro
        FROM matriculas m
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.fecha_registro DESC
    """)
    matriculas = cursor.fetchall()

    # Obtener lista de usuarios para el select
    cursor.execute("SELECT id, nombre, apellidos, email FROM usuarios")
    usuarios = [
        {'id': row[0], 'nombre': row[1], 'apellidos': row[2], 'email': row[3]}
        for row in cursor.fetchall()
    ]

    conexion.close()

    return render_template('admin_matriculas.html', matriculas=matriculas, usuarios=usuarios)

@auth.route('/admin/editar_matricula', methods=['POST'])
@login_required
@solo_admin
def editar_matricula():
    matricula_id = request.form.get('matricula_id')
    nueva_matricula = request.form.get('nueva_matricula', '').upper()

    if not re.fullmatch(r'\d{4}[A-Z]{3}', nueva_matricula):
        flash("Formato de matrícula no válido. Usa 4 números seguidos de 3 letras (ej: 1234ABC).", "danger")
        return redirect(url_for('auth.matriculas_admin'))

    conexion = conectar_db()
    cursor = conexion.cursor()

    # Validar que no haya otra matrícula con ese mismo valor
    cursor.execute("SELECT id FROM matriculas WHERE matricula = %s AND id != %s", (nueva_matricula, matricula_id))
    if cursor.fetchone():
        conexion.close()
        flash("Ya existe otra matrícula con ese valor.", "danger")
        return redirect(url_for('auth.matriculas_admin'))

    # Solo permitir editar si está autorizada
    cursor.execute("UPDATE matriculas SET matricula = %s WHERE id = %s AND estado = 'autorizada'", (nueva_matricula, matricula_id))
    conexion.commit()
    conexion.close()

    flash("Matrícula actualizada correctamente.", "success")
    return redirect(url_for('auth.matriculas_admin'))


@auth.route('/admin/eliminar_matricula/<int:matricula_id>', methods=['POST'], endpoint='eliminar_matricula_admin')
@login_required
@solo_admin
def eliminar_matricula_admin(matricula_id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM matriculas WHERE id = %s", (matricula_id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula eliminada correctamente.", "success")
    return redirect(url_for('auth.matriculas_admin'))
