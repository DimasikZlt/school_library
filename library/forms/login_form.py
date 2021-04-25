from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(
        'Адрес электронной почты',
        description='user@yandex.ru',
        validators=[
            InputRequired('Пожалуйста введите Ваш адрес электронной почты.'),
            Email('Поле должно содержать действительный адрес электронной почты.')
        ])
    password = PasswordField('Пароль', validators=[InputRequired()])
    submit = SubmitField('Войти')
