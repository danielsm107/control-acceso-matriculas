# routes/matriculas.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from utils.db_utils import conectar_db
import re

matriculas = Blueprint('matriculas', __name__)

@matriculas.route('/mis_matriculas')
@login_required
def mis_matriculas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT matricula, estado, id FROM matriculas WHERE usuario_id = %s", (current_user.id,))
    datos = cursor.fetchall()
    conexion.close()

    return render_template('mis_matriculas.html', matriculas=datos)


@matriculas.route('/solicitar_matricula', methods=['GET', 'POST'])
@login_required
def solicitar_matricula():
    def _redirect_matriculas():
        if current_user.rol == 'admin':
            return redirect(url_for('admin.matriculas_admin'))
        else:
            return redirect(url_for('main.index'))

    if request.method == 'POST':
        matricula = request.form['matricula'].upper()

        if not re.fullmatch(r'\d{4}[A-Z]{3}', matricula):
            flash('Formato de matrícula no válido. Debe ser 4 números seguidos de 3 letras (ej: 1234ABC).', 'danger')
            return _redirect_matriculas()

        conexion = conectar_db()
        cursor = conexion.cursor()

        usuario_id = current_user.id
        if current_user.rol == 'admin':
            usuario_id_form = request.form.get('usuario_id')
            if usuario_id_form and usuario_id_form.isdigit():
                usuario_id = int(usuario_id_form)

        cursor.execute("SELECT COUNT(*) FROM matriculas WHERE matricula = %s AND usuario_id = %s", (matricula, usuario_id))
        existe_para_usuario = cursor.fetchone()[0]

        if existe_para_usuario:
            conexion.close()
            flash('Esa matrícula ya está registrada para ese usuario.', 'danger')
            return _redirect_matriculas()

        cursor.execute("SELECT COUNT(*) FROM matriculas WHERE matricula = %s", (matricula,))
        ya_existe_global = cursor.fetchone()[0]

        if ya_existe_global:
            conexion.close()
            flash("Esa matrícula ya ha sido registrada por otro usuario.", "danger")
            return _redirect_matriculas()

        estado = 'autorizada' if current_user.rol == 'admin' and usuario_id != current_user.id else 'pendiente'

        cursor.execute(
            "INSERT INTO matriculas (matricula, estado, usuario_id) VALUES (%s, %s, %s)",
            (matricula, estado, usuario_id)
        )
        conexion.commit()
        conexion.close()

        if current_user.rol == 'admin':
            flash(f'Matrícula registrada y autorizada para el usuario ID {usuario_id}.', 'success')
            return redirect(url_for('admin.matriculas_admin'))
        else:
            flash('Matrícula solicitada correctamente. Pendiente de aprobación.', 'success')
            return redirect(url_for('main.index'))

    return render_template('solicitar_matricula.html')


@matriculas.route('/eliminar_matricula/<int:matricula_id>', methods=['POST'])
@login_required
def eliminar_matricula(matricula_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM matriculas 
        WHERE id = %s AND usuario_id = %s AND estado IN ('denegada', 'pendiente')
    """, (matricula_id, current_user.id))
    
    if cursor.rowcount > 0:
        flash('Matrícula eliminada correctamente.', 'success')
    else:
        flash('No se pudo eliminar la matrícula.', 'danger')

    conexion.commit()
    conexion.close()

    return redirect(url_for('main.index'))
