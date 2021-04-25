import flask
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from library.forms.order_form import AdminOrderForm, UserOrderForm
from library.forms.warning_form import WarningForm
from library.models.book import Book
from library import db
from library.models.user import User

blueprint = flask.Blueprint('orders', __name__, template_folder='templates')


def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if not book:
        return redirect(url_for('orders.get_orders'))
    return book


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('orders.get_orders'))
    return user


@blueprint.route('/orders')
@login_required
def get_orders():
    headers = (
        '№',
        'Пользователь',
        'Книга',
        'Автор',
        'Вернуть',
    )
    db_fields = (User.last_name, User.first_name)
    if current_user.is_admin:
        users = User.query.join(User.books).order_by(*db_fields, Book.title).all()
    else:
        users = User.query.filter_by(id=current_user.id).join(User.books).order_by(Book.title).all()
    if users:
        return render_template(
            'orders.html',
            headers=headers,
            users=users,
            caption_table='Журнал учета книг'
        )
    return redirect(url_for('orders.add_order'))


@blueprint.route('/orders/new/', methods=['GET', 'POST'])
@login_required
def add_order():
    if current_user.is_admin:
        form = AdminOrderForm()
    else:
        form = UserOrderForm()
        form.users.data = current_user
    if form.cancel.data:
        return redirect(url_for('orders.get_orders'))
    if form.validate_on_submit():
        book = form.books.data
        user = form.users.data
        user.books.append(book)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        finally:
            return redirect(url_for('orders.get_orders'))
    return render_template('order_form.html', form=form)


@blueprint.route('/orders/<int:book_id>/user/<int:user_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_order(book_id, user_id):
    book = get_book_by_id(book_id)
    user = get_user_by_id(user_id)
    form = WarningForm()
    if form.cancel.data:
        return redirect(url_for('orders.get_orders'))
    if form.validate_on_submit():
        user.books.remove(book)
        db.session.commit()
        return redirect(url_for('orders.get_orders'))
    return render_template(
        'info_form.html',
        form=form,
        title='Вернуть книгу?',
        message='Вы действительно хотите вернуть книгу?',
        obj=f"{book.author} {book.title}"
    )
