# routes/admin.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from utils.db_utils import conectar_db
import re
from functools import wraps

admin = Blueprint('admin', __name__)

# Decorador para verificar rol admin
def solo_admin(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'rol' not in session or session['rol'] != 'admin':
            flash("Acceso denegado. Solo el administrador puede ver esta página.", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorador

@admin.route("/admin/cambiar_rol/<int:user_id>", methods=["POST"])
@login_required
def cambiar_rol(user_id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("index"))

    if user_id == 8:  # ID del administrador principal
        flash("No se puede modificar el rol del administrador principal.", "warning")
        return redirect(url_for("admin.admin_panel"))

    nuevo_rol = request.form.get("rol")
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, user_id))
    conexion.commit()
    conexion.close()

    flash("Rol actualizado correctamente", "success")
    return redirect(url_for("admin.admin_panel"))

@admin.route("/admin")
@login_required
def admin_panel():
    if current_user.rol != 'admin':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('main.index'))
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre, apellidos, email, rol FROM usuarios")
    users = cursor.fetchall()

    cursor.execute("""
        SELECT m.id, m.matricula, u.nombre, u.apellidos, u.email, m.estado
        FROM matriculas m
        JOIN usuarios u ON m.usuario_id = u.id
        WHERE m.estado = 'pendiente'
    """)
    pendientes = cursor.fetchall()

    conexion.close()
    return render_template("admin_panel.html", users=users, pendientes=pendientes, user=current_user)

@admin.route('/matriculas_admin')
@login_required
@solo_admin
def matriculas_admin():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT m.id, m.matricula, u.nombre, u.apellidos, u.email, m.estado, m.fecha_registro
        FROM matriculas m
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.fecha_registro DESC
    """)
    matriculas = cursor.fetchall()

    cursor.execute("SELECT id, nombre, apellidos, email FROM usuarios")
    usuarios = [
        {'id': row[0], 'nombre': row[1], 'apellidos': row[2], 'email': row[3]}
        for row in cursor.fetchall()
    ]

    conexion.close()
    return render_template('admin_matriculas.html', matriculas=matriculas, usuarios=usuarios)

@admin.route('/admin/editar_matricula', methods=['POST'])
@login_required
@solo_admin
def editar_matricula():
    matricula_id = request.form.get('matricula_id')
    nueva_matricula = request.form.get('nueva_matricula', '').upper()

    if not re.fullmatch(r'\d{4}[A-Z]{3}', nueva_matricula):
        flash("Formato de matrícula no válido. Usa 4 números seguidos de 3 letras (ej: 1234ABC).", "danger")
        return redirect(url_for('admin.matriculas_admin'))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM matriculas WHERE matricula = %s AND id != %s", (nueva_matricula, matricula_id))
    if cursor.fetchone():
        conexion.close()
        flash("Ya existe otra matrícula con ese valor.", "danger")
        return redirect(url_for('admin.matriculas_admin'))

    cursor.execute("UPDATE matriculas SET matricula = %s WHERE id = %s AND estado = 'autorizada'", (nueva_matricula, matricula_id))
    conexion.commit()
    conexion.close()

    flash("Matrícula actualizada correctamente.", "success")
    return redirect(url_for('admin.matriculas_admin'))

@admin.route('/admin/eliminar_matricula/<int:matricula_id>', methods=['POST'], endpoint='eliminar_matricula_admin')
@login_required
@solo_admin
def eliminar_matricula_admin(matricula_id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM matriculas WHERE id = %s", (matricula_id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula eliminada correctamente.", "success")
    return redirect(url_for('admin.matriculas_admin'))

@admin.route("/admin/eliminar_usuario/<int:user_id>", methods=["POST"])
@login_required
def eliminar_usuario(user_id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("admin.admin_panel"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    conexion.commit()
    conexion.close()

    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for("admin.admin_panel"))

@admin.route("/admin/aprobar/<int:id>", methods=["POST"])
@login_required
def aprobar_matricula(id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("admin.admin_panel"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE matriculas SET estado = 'autorizada' WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula aprobada", "success")
    return redirect(url_for("admin.admin_panel"))

@admin.route("/admin/rechazar/<int:id>", methods=["POST"])
@login_required
def rechazar_matricula(id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("admin.admin_panel"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE matriculas SET estado = 'denegada' WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula rechazada", "warning")
    return redirect(url_for("admin.admin_panel"))

@admin.route('/limpiar_historial', methods=['POST'])
@login_required
def limpiar_historial():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('main.historial'))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM registros_accesos")
    conexion.commit()
    conexion.close()

    flash('Historial de accesos eliminado correctamente.', 'success')
    return redirect(url_for('main.historial'))
