import flask
from flask import render_template

blueprint = flask.Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/')
@blueprint.route('/about')
def about():
    return render_template('about.html')
