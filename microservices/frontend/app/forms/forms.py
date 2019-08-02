from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField


class SubmitStockForm(FlaskForm):
    stock = StringField('New Stock')
    logo = FileField('Upload Logo')
    submit = SubmitField('Submit')
