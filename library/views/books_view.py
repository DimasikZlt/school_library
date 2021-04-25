import flask
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from library.forms.book_form import NewBookForm, EditBookForm
from library.forms.warning_form import WarningForm
from library.models.author import Author
from library.models.book import Book
from library import db

blueprint = flask.Blueprint('books', __name__, template_folder='templates')


def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if not book:
        return redirect(url_for('books.get_books'))
    return book


def get_author_by_id(author_id):
    author = Author.query.get(author_id)
    if not author:
        return redirect(url_for('books.get_books'))
    return author


@blueprint.route('/books')
@login_required
def get_books():
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    headers = (
        '№',
        'Автор',
        'Название',
        'Изменить',
        'Удалить',
    )
    db_fields = (Author.last_name, Author.first_name, Author.middle_name)
    authors = Author.query.join(Author.books).order_by(*db_fields, Book.title).all()
    if authors:
        return render_template(
            'books.html',
            headers=headers,
            authors=authors,
            caption_table='Книги'
        )
    return redirect(url_for('books.add_book'))


@blueprint.route('/books/new/', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    form = NewBookForm()
    if form.cancel.data:
        return redirect(url_for('books.get_books'))
    if form.validate_on_submit():
        new_book = Book(title=form.title.data)
        form.authors.data.books.append(new_book)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        finally:
            return redirect(url_for('books.get_books'))
    return render_template('book_form.html', form=form)


@blueprint.route('/books/<int:book_id>/author/<int:author_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_book(book_id, author_id):
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    form = EditBookForm()
    book = get_book_by_id(book_id)
    if form.cancel.data:
        return redirect(url_for('books.get_books'))
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        return redirect(url_for('books.get_books'))
    author = get_author_by_id(author_id)
    form.authors.data = f"{author.last_name} {author.first_name[0]}. {author.middle_name[0]}."
    form.title.data = book.title
    return render_template('book_form.html', form=form)


@blueprint.route('/books/<int:book_id>/author<int:author_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_book(book_id, author_id):
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    book = get_book_by_id(book_id)
    form = WarningForm()
    if form.cancel.data:
        return redirect(url_for('books.get_books'))
    if form.validate_on_submit():
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('books.get_books'))
    author = get_author_by_id(author_id)
    return render_template(
        'warning_form.html',
        form=form,
        title='Удаление книги?',
        message='Вы действительно хотите удалить унигу?',
        obj=f"{author.last_name} {author.first_name[0]}. {author.middle_name[0]}. {book.title}"
    )
