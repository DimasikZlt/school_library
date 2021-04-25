from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from library.models.book import Book
from library.models.user import User


class AdminOrderForm(FlaskForm):
    users = QuerySelectField(
        'Выберите пользоватя из списка',
        query_factory=lambda:
        User.query.order_by(User.last_name, User.first_name).all()
    )

    books = QuerySelectField(
        'Выберите книгу из списка',
        query_factory=lambda:
        Book.query.order_by(Book.title).all()
    )

    submit = SubmitField('OK')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})


class UserOrderForm(FlaskForm):
    users = StringField('Пользователь', render_kw={'readonly': True})
    books = QuerySelectField(
        'Выберите книгу из списка',
        query_factory=lambda:
        Book.query.order_by(Book.title).all()
    )

    submit = SubmitField('OK')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})
