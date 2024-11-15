"""gallery"""
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import Base


# noinspection PyUnresolvedReferences
class Gallery(Base):  # pylint: disable=too-few-public-methods
    """Gallery model"""
    __tablename__ = 'gallery'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(140))
    albums: Mapped[List["Album"]] = relationship(  # type: ignore # noqa: F821
        back_populates='gallery'
    )

    def __repr__(self):
        return f'<Gallery {self.name}>'
