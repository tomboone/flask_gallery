"""album"""
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import Base


# noinspection PyUnresolvedReferences
class Album(Base):  # pylint: disable=too-few-public-methods
    """Album model"""
    __tablename__ = 'album'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    gallery_id: Mapped[int] = mapped_column(ForeignKey('gallery.id'))
    gallery: Mapped["Gallery"] = relationship(  # noqa: F821
        back_populates='albums'
    )
    images: Mapped[List["Image"]] = relationship(  # noqa: F821
        back_populates='album'
    )

    def __repr__(self):
        return f'<Album {self.name}>'
