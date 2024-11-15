"""User"""
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class User(Model):  # pylint: disable=too-few-public-methods
    """User model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    def __repr__(self):
        return f'<User {self.email}>'
