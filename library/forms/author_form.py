from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class AuthorForm(FlaskForm):
    first_name = StringField(
        'Имя',
        description='Имя автора',
        validators=[
            InputRequired('Пожалуйста введите имя автора.'),
            Length(
                min=2,
                max=50,
                message="Имя должно быть не менне 2 и не больее 50 символов."
            )
        ])
    middle_name = StringField(
        'Отчество',
        description='Отчество автора',
        validators=[
            InputRequired('Пожалуйста введите отчество автора.'),
            Length(
                min=1,
                max=50,
                message="Отчество должно быть не менне 2 и не больее 50 символов."
            )
        ])
    last_name = StringField(
        'Фамилия',
        description='Фамилия автора',
        validators=[
            InputRequired('Пожалуйста введите фамилию автора.'),
            Length(
                min=3,
                max=50,
                message="Фамилия должна быть не менне 2 и не больее 50 символов."
            )
        ])
    submit = SubmitField('OK')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})
