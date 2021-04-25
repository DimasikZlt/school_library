import flask
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from library.forms.user_form import UserForm, NewUserForm
from library.forms.warning_form import WarningForm
from library import db
from library.models.user import User

blueprint = flask.Blueprint('users', __name__, template_folder='templates')


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('users.get_users'))
    return user


@blueprint.route('/users')
@login_required
def get_users():
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    headers = (
        '№',
        'Фамилия',
        'Имя',
        'Электронная почта',
        'Изменить',
        'Удалить',
    )
    users = User.query.order_by(User.last_name, User.first_name, User.email).all()
    if users:
        return render_template(
            'users.html',
            headers=headers,
            users=users,
            caption_table='Пользователи'
        )
    return redirect(url_for('users.add_user'))


@blueprint.route('/users/new/', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    form = NewUserForm()
    if form.cancel.data:
        return redirect(url_for('users.get_users'))
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,    # noqa
            last_name=form.last_name.data,  # noqa
            email=form.email.data,  # noqa
            is_admin=form.is_admin.data # noqa
        )
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        finally:
            return redirect(url_for('users.get_users'))
    return render_template('user_form.html', form=form)


@blueprint.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    user = get_user_by_id(user_id)
    form = UserForm(obj=user)
    if form.cancel.data:
        return redirect(url_for('users.get_users'))
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('users.get_users'))
    return render_template('user_form.html', form=form)


@blueprint.route('/users/<int:user_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return render_template('forbidden.html'), 403
    user = get_user_by_id(user_id)
    form = WarningForm()
    if form.cancel.data:
        return redirect(url_for('users.get_users'))
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users.get_users'))
    return render_template(
        'warning_form.html',
        form=form,
        title='Удаление пользователя?',
        message='Вы действительно хотите удалить пользователя?',
        obj=f"{user.first_name} {user.last_name}, {user.email}"
    )
