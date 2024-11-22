"""extensions"""
from flask_login import LoginManager  # type: ignore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

login_manager = LoginManager()
