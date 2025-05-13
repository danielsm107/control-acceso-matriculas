# routes/admin.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from utils.db_utils import conectar_db

admin = Blueprint('admin', __name__)

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


@admin.route("/admin/aprobar/<int:id>", methods=["POST"])
@login_required
def aprobar_matricula(id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("main.index"))

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
        return redirect(url_for("main.index"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE matriculas SET estado = 'denegada' WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

    flash("Matrícula rechazada", "warning")
    return redirect(url_for("admin.admin_panel"))


@admin.route("/admin/eliminar_usuario/<int:user_id>", methods=["POST"])
@login_required
def eliminar_usuario(user_id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("main.index"))

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    conexion.commit()
    conexion.close()

    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for("admin.admin_panel"))


@admin.route("/admin/cambiar_rol/<int:user_id>", methods=["POST"])
@login_required
def cambiar_rol(user_id):
    if current_user.rol != "admin":
        flash("Acceso no autorizado", "danger")
        return redirect(url_for("main.index"))

    if user_id == 8:
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
