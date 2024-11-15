"""album"""
from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models.image import Image


class Album(db.Model):  # pylint: disable=too-few-public-methods
    """Album model"""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    gallery: Mapped[int] = mapped_column(Integer, ForeignKey('gallery.id'))
    images: Mapped[List['Image']] = relationship(back_populates='album')

    def __repr__(self):
        return f'<Album {self.name}>'
