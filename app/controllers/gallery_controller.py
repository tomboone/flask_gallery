""" Gallery controller """
from app.models.gallery import Gallery
from app.extensions import db


class GalleryController:
    """ Gallery controller """

    @staticmethod
    def get_all_galleries():
        """ Get all galleries """
        return db.session.execute(db.select(Gallery)).scalars().all()

    @staticmethod
    def get_gallery(gallery_id):
        """ Get gallery """
        return db.session.execute(db.select(Gallery).filter_by(id=gallery_id)).scalar_one_or_none()
