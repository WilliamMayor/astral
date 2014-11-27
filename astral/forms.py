from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class SetupForm(Form):
    directory = StringField(u'Storage Directory', validators=[DataRequired()])
