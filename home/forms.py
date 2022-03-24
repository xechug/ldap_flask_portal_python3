# The code above is a class that inherits from FlaskForm. 
# 
# The class is a form that has fields that are required. 
# 
# The fields are a string field, a password field, a select field, a date time field, a text area
# field, and a submit field.
# 
# The code below is a class that inherits from FlaskForm. Exemple:
# 
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired()])
#     password = PasswordField('Password', valid

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateTimeField, validators, TextAreaField, SubmitField
from wtforms.validators import InputRequired

#from wtforms.fields.html5 import DateField, TimeField
#from datetime import date, datetime


# This is creating a form that will be used to send a notification to a user in panel /home.
# This form enables the user to send a notification to a user.

class CreateNotify(FlaskForm):
    type = SelectField('Escoge tipo de alerta : ' ,validators=[InputRequired()], choices=[(1,"Información general"),(2,"Alerta"), (3,"Notificación")], render_kw={'class': 'form-control'})
    datatime_start = DateTimeField('Fecha de notificación Inicio: ', format="%Y-%m-%d %H:%M:%S", ## Now it will call it everytime.
        validators=[validators.DataRequired()], render_kw={'class': 'form-control datetimepicker form_datetime', 'readonly': True})
    datatime_end = DateTimeField('Fecha de notificación Final: ', format="%Y-%m-%d %H:%M:%S", ## Now it will call it everytime.
        validators=[validators.DataRequired()], render_kw={'class': 'form-control datetimepicker form_datetime', 'readonly': True})
    message= TextAreaField('Mensaje a mostrar',validators=[InputRequired()],render_kw={'cols':11,'class': 'form-control'})
    submit = SubmitField(label="Enviar", render_kw={'class':"btn btn-primary"})