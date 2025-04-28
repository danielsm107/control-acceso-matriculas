from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_utils import conectar_db, User
from forms import RegisterForm

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
    form = RegisterForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        apellidos = form.apellidos.data
        email = form.email.data
        password = form.password.data

        password_hashed = generate_password_hash(password)

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellidos, email, password, rol) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellidos, email, password_hashed, 'usuario')
        )
        conexion.commit()
        conexion.close()

        flash('Cuenta creada correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)