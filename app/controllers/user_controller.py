""" User controller """
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db


class UserController:
    """ User controller """

    @staticmethod
    def create_user(email, password):
        """ Create user """
        user = User(email=email, password=generate_password_hash(password))
        return user

    @staticmethod
    def user_login(email, password):
        """ User login """
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user and check_password_hash(user.password, password):
            return user
        return None
