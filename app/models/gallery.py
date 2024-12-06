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
class Gallery(Model):
    """Gallery model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    albums: Mapped[List["Album"]] = relationship(  # type: ignore # noqa: F821
        back_populates='gallery'
    )

    def __repr__(self):
        return f'<Gallery {self.name}>'

    @staticmethod
    def get_all_galleries():
        """ Get all galleries """
        return db.session.execute(db.select(Gallery).order_by(Gallery.name)).scalars().all()

    @staticmethod
    def get_gallery(gallery_id):
        """ Get gallery """
        return db.session.execute(db.select(Gallery).filter_by(id=gallery_id)).scalar_one_or_none()

    @staticmethod
    def get_gallery_by_slug(slug):
        """ Get gallery by slug """
        return db.session.execute(db.select(Gallery).filter_by(slug=slug)).scalar_one_or_none()
