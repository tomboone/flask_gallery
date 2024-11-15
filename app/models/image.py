"""image"""
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import Base


# noinspection PyUnresolvedReferences
class Image(Base):  # pylint: disable=too-few-public-methods
    """Image model"""
    __tablename__ = 'image'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    album_id: Mapped[int] = mapped_column(ForeignKey('album.id'))
    album: Mapped["Album"] = relationship(  # noqa: F821
        back_populates='images'
    )

    def __repr__(self):
        return f'<Image {self.name}>'
