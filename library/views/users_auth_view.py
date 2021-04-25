import flask
from flask import redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from library.forms.login_form import LoginForm
from library.models.user import User

blueprint = flask.Blueprint('users_auth', __name__, template_folder='templates')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('orders.get_orders'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_password_ok(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('orders.get_orders'))
        else:
            flash('Неверный email или пароль', 'danger')
    return render_template('login_form.html', title='Вход', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('about.about'))
