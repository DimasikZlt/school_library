from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, ValidationError

from library.models.user import User


class UserFormBase(FlaskForm):
    first_name = StringField(
        'Имя',
        description='Ваше имя',
        validators=[
            InputRequired('Пожалуйста введите имя.'),
            Length(
                min=3, max=25,
                message="Имя должно быть не менне 3 и не больее 25 символов."
            )
        ])
    last_name = StringField(
        'Фамилия',
        description='Ваша фамилия',
        validators=[
            InputRequired('Пожалуйста введите фамилию.'),
            Length(
                min=3,
                max=25,
                message="Фамилия должна быть не менне 3 и не больее 25 символов."
            )
        ])
    is_admin = BooleanField('Роль Администратора')
    submit = SubmitField('OK')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})


class UserForm(UserFormBase):
    email = StringField(
        'Адрес электронной почты',
        description='user@yandex.ru',
        render_kw={'readonly': True}
        )

    password = PasswordField(
        'Новый пароль',
        description='Сменить пароль',
        validators=[
            Optional('Пожалуйста введите новый пароль.'),
            EqualTo('confirm', message="Пароли должны совпадать."),
            Length(
                min=3,
                max=12,
                message="Пароль должен быть не менне 3 и не больее 12 символов."
            )
        ])
    confirm = PasswordField('Повторите пароль', description='Повторите пароль', )


class NewUserForm(UserFormBase):
    email = StringField(
        'Адрес электронной почты',
        description='user@yandex.ru',
        validators=[
            InputRequired('Пожалуйста введите Ваш адрес электронной почты.'),
            Email('Поле должно содержать действительный адрес электронной почты.'),
            Length(
                max=50,
                message="Адрес электронной почты должен быть не больее 100 символов."
            )
        ])
    password = PasswordField(
        'Новый пароль',
        description='Задайте пароль',
        validators=[
            InputRequired('Пожалуйста введите новый пароль.'),
            EqualTo('confirm', message="Пароли должны совпадать."),
            Length(
                min=3,
                max=12,
                message="Пароль должен быть не менне 3 и не больее 12 символов."
            )
        ])
    confirm = PasswordField('Повторите пароль', description='Повторите пароль', )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Пользователь с таким адресом электронной почты уже существует!')
