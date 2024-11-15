"""extensions"""
from flask_login import LoginManager  # type: ignore
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy(model_class=DeclarativeBase)

login_manager = LoginManager()
