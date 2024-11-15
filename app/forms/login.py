"""login form"""
from flask_wtf import FlaskForm  # type: ignore
from wtforms.fields.simple import StringField, BooleanField, SubmitField  # type: ignore
from wtforms.validators import DataRequired, Email  # type: ignore


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
