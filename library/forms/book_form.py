from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length

from library.models.author import Author


class NewBookForm(FlaskForm):
    authors = QuerySelectField(
        'Выберите автора из списка',
        query_factory=lambda:
        Author.query.order_by(Author.last_name, Author.first_name, Author.middle_name).all()
    )
    title = StringField(
        'Название книги',
        description='Название книги',
        validators=[
            InputRequired('Пожалуйста введите название книги автора.'),
            Length(
                min=3,
                max=120,
                message="название книги должно быть не менне 3 и не больее 120 символов."
            )
        ])

    submit = SubmitField('OK')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})


class EditBookForm(FlaskForm):
    authors = StringField('Автор', render_kw={'readonly': True})
    title = StringField(
        'Название книги',
        description='Название книги',
        validators=[
            InputRequired('Пожалуйста введите название книги автора.'),
            Length(
                min=3,
                max=120,
                message="название книги должно быть не менне 3 и не больее 120 символов."
            )
        ])

    submit = SubmitField('OK')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})
