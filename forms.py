
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class QrForm(FlaskForm):
    name = StringField('Введите текст...')
    submit = SubmitField('Применить')


class SignIn(FlaskForm):
    login = StringField('Введите логин...')
    password = PasswordField('Введите пароль...')
    submit = SubmitField('Войти')

class SignUp(FlaskForm):
    login = StringField('Придумайте логин...')
    password = PasswordField('Придумайте пароль...')
    submit = SubmitField('Регистрация')

class Send(FlaskForm):
    submit = SubmitField('Сохранить на аккаунт')