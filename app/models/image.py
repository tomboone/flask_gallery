"""image"""
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


# noinspection PyUnresolvedReferences
class Image(Model):  # pylint: disable=too-few-public-methods
    """Image model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(64), unique=True)
    caption: Mapped[str] = mapped_column(String(2200))
    album_id: Mapped[int] = mapped_column(ForeignKey('album.id'))
    album: Mapped["Album"] = relationship(  # type: ignore # noqa: F821
        back_populates='images'
    )

    def __repr__(self):
        return f'<Image {self.name}>'
