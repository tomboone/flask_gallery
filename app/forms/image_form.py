"""
Image form
"""
from flask_wtf import FlaskForm  # type:ignore
from flask_wtf.file import FileAllowed, FileRequired  # type:ignore
from wtforms import FileField, StringField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    """
    Image form
    """
    image = FileField('Image', validators=[DataRequired(), FileRequired(), FileAllowed(['jpg', 'jpeg'])])
    caption = StringField('Caption')
