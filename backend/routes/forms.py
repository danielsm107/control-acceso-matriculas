from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from utils.db_utils import conectar_db

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_email(self, field):
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (field.data,))
        existing_user = cursor.fetchone()
        conexion.close()
        if existing_user:
            raise ValidationError('Este correo ya está registrado.')