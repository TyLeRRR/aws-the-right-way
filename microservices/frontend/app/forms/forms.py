from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class SubmitStockForm(FlaskForm):
    stock = StringField('New Stock', validators=[DataRequired()])
    logo = FileField('Upload Logo', validators=[DataRequired()])
    submit = SubmitField('Submit')
