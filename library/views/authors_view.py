import flask
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from library.forms.author_form import AuthorForm
from library.forms.warning_form import WarningForm
from library import db
from library.models.author import Author

blueprint = flask.Blueprint('authors', __name__, template_folder='templates')


def get_author_by_id(author_id):
    author = Author.query.get(author_id)
    if not author:
        return redirect(url_for('authors.get_authors'))
    return author


@blueprint.route('/authors')
@login_required
def get_authors():
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    headers = (
        '№',
        'Фамилия',
        'Имя',
        'Отчество',
        'Изменить',
        'Удалить',
    )
    authors = Author.query.order_by(Author.last_name, Author.first_name, Author.middle_name).all()
    if authors:
        return render_template(
            'authors.html',
            headers=headers,
            authors=authors,
            caption_table='Авторы'
        )
    return redirect(url_for('authors.add_author'))


@blueprint.route('/authors/new/', methods=['GET', 'POST'])
@login_required
def add_author():
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    form = AuthorForm()
    if form.cancel.data:
        return redirect(url_for('authors.get_authors'))
    if form.validate_on_submit():
        new_author = Author(
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
        )
        try:
            db.session.add(new_author)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        finally:
            return redirect(url_for('authors.get_authors'))
    return render_template('author_form.html', form=form)


@blueprint.route('/authors/<int:author_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    author = get_author_by_id(author_id)
    form = AuthorForm(obj=author)
    if form.cancel.data:
        return redirect(url_for('authors.get_authors'))
    if form.validate_on_submit():
        form.populate_obj(author)
        db.session.commit()
        return redirect(url_for('authors.get_authors'))
    return render_template('author_form.html', form=form)


@blueprint.route('/authors/<int:author_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_author(author_id):
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    author = get_author_by_id(author_id)
    form = WarningForm()
    if form.cancel.data:
        return redirect(url_for('authors.get_authors'))
    if form.validate_on_submit():
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('authors.get_authors'))
    return render_template(
        'warning_form.html',
        form=form,
        title='Удаление автора?',
        message='Вы действительно хотите удалить автора?',
        obj=f"{author.last_name} {author.first_name[0]}. {author.middle_name[0]}."
    )
