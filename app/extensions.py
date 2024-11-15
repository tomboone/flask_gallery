"""extensions"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Base class for all models"""
    pass  # pylint: disable=unnecessary-pass


db = SQLAlchemy(model_class=Base)
