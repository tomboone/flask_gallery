"""image"""
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class Image(db.Model):  # pylint: disable=too-few-public-methods
    """Image model"""
    __tablename__ = 'image'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    album_id: Mapped[int] = mapped_column(Integer, ForeignKey('album.id'))

    def __repr__(self):
        return f'<Image {self.name}>'
