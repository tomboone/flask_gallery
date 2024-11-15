"""gallery"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


# noinspection PyUnresolvedReferences
class Gallery(Model):  # pylint: disable=too-few-public-methods
    """Gallery model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    albums: Mapped[List["Album"]] = relationship(  # type: ignore # noqa: F821
        back_populates='gallery'
    )

    def __repr__(self):
        return f'<Gallery {self.name}>'
