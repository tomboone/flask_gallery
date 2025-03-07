"""
Image form
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, StringField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    """
    Image form
    """
    image = FileField('Image', validators=[DataRequired(), FileRequired(), FileAllowed(['jpg', 'jpeg'])])
    caption = StringField('Caption')
