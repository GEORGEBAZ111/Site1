from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_retry = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Создать аккаунт')


class SearchForm(FlaskForm):
    req = StringField('Поисковой запрос', validators=[DataRequired()])
    submit = SubmitField('Найти')