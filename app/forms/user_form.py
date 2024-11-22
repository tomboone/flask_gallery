"""
User form
"""
from flask_login import UserMixin  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from wtforms.fields.simple import StringField, PasswordField  # type: ignore
from wtforms.validators import DataRequired, Email  # type: ignore


class UserForm(FlaskForm, UserMixin):
    """
    User form
    """
    email = StringField(  # email field
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    current_password = PasswordField('Current Password')  # current password field
    new_password = PasswordField('New Password')  # new password field
    confirm_password = PasswordField('Confirm New Password')  # confirm password field
