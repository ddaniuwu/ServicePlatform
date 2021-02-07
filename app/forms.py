from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField , FileRequired , FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Número de control', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')



class TodoForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Crear')



class StudentForm(FlaskForm):
    submit = SubmitField('Inscribirme al programa de Servicio Social')



class UploadForm(FlaskForm):
    Folder_name = StringField('Nombre de la carpeta ' , validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    SubmitField = SubmitField('Subir')