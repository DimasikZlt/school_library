from flask_wtf import FlaskForm
from wtforms import SubmitField


class WarningForm(FlaskForm):
    submit = SubmitField('Удалить')
    cancel = SubmitField('Отмена', render_kw={'formnovalidate': True})
