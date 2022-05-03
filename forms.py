
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class QrForm(FlaskForm):
    name = StringField('Введите текст...')
    submit = SubmitField('Применить')