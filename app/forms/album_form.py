"""
Album form
"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms.fields.simple import StringField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class AlbumForm(FlaskForm):
    """
    Album form
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
