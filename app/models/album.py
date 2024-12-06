"""album"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


# noinspection PyUnresolvedReferences
class Album(Model):  # pylint: disable=too-few-public-methods
    """Album model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    gallery_id: Mapped[int] = mapped_column(ForeignKey('gallery.id'))
    gallery: Mapped["Gallery"] = relationship(  # type: ignore # noqa: F821
        back_populates='albums'
    )
    images: Mapped[List["Image"]] = relationship(  # type: ignore # noqa: F821
        back_populates='album'
    )

    def __repr__(self):
        return f'<Album {self.name}>'

    @staticmethod
    def get_album(album_id):
        """ Get album """
        return db.session.execute(db.select(Album).filter_by(id=album_id)).scalar_one_or_none()

    @staticmethod
    def get_album_by_slug(slug):
        """ Get album by slug """
        return db.session.execute(db.select(Album).filter_by(slug=slug)).scalar_one_or_none()
