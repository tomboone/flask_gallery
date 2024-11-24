"""
Gallery routes
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required  # type: ignore
from app.extensions import db
from app.forms.album_form import AlbumForm  # type: ignore
from app.forms.gallery_form import GalleryForm
from app.models.album import Album
from app.models.gallery import Gallery

bp = Blueprint('gallery', __name__)


@bp.route('/')
def index():
    """
    Gallery index

    :return: gallery index
    """
    return render_template(
        'gallery/index.html',  # template
        galleries=Gallery.get_all_galleries(),  # galleries
        title='Galleries'  # title
    )


@bp.route('/new-gallery', methods=['GET', 'POST'])
@login_required
def c_gallery():
    """
    Create gallery

    :return: new gallery form
    """
    form = GalleryForm()  # create form instance

    if form.validate_on_submit():  # if form is submitted
        gallery = Gallery(  # create gallery
            form.name.data,
            form.description.data
        )
        db.session.add(gallery)
        db.session.commit()
        flash(  # flash message
            'Gallery created',
            'success'
        )
        return redirect(  # redirect to gallery index
            url_for('gallery.index')
        )
    return render_template(  # render new gallery form
        'gallery/gallery/form.html',
        form=form,
        title='New Gallery'
    )


@bp.route('/gallery-<gallery_id>')
def r_gallery(gallery_id):
    """
    Read gallery/Albums index

    :param gallery_id: gallery id

    :return: gallery
    """
    gallery = Gallery.get_gallery(gallery_id)  # get gallery

    if not gallery:  # if gallery not found
        flash(  # flash message
            'Gallery not found',
            'danger'
        )
        return redirect(  # redirect to gallery index
            url_for('gallery.index')
        )

    return render_template(  # render gallery
        'gallery/gallery/index.html',  # template
        gallery=gallery,  # gallery
        title=gallery.name  # title
    )


@bp.route('/gallery-<gallery_id>/edit')
@login_required
def u_gallery(gallery_id):
    """
    Update gallery

    :param gallery_id: gallery id

    :return: edit gallery form
    """
    gallery = Gallery.get_gallery(gallery_id)  # get gallery

    if not gallery:  # if gallery not found
        flash(  # flash message
            'Gallery not found',
            'danger'
        )
        return redirect(  # redirect to gallery index
            url_for('gallery.index')
        )

    form = GalleryForm(obj=gallery)  # create form instance

    if form.validate_on_submit():  # if form is submitted, update gallery

        gallery.name = form.name.data  # name
        gallery.description = form.description.data  # description

        db.session.commit()  # commit changes

        flash(  # flash message
            'Gallery updated',
            'success'
        )

        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_id=gallery_id
            )
        )

    return render_template(  # render edit gallery form
        'gallery/gallery/form.html',  # template
        gallery=gallery,  # gallery
        form=form,  # form
        title='Edit Gallery'  # title
    )


@bp.route('/gallery-<gallery_id>/delete', methods=['GET', 'POST'])
@login_required
def d_gallery(gallery_id):
    """
    Delete gallery

    :param gallery_id: gallery id

    :return: delete gallery
    """
    gallery = Gallery.get_gallery(gallery_id)  # get gallery

    if not gallery:  # if gallery not found
        flash(  # flash message
            'Gallery not found',
            'danger'
        )
        return redirect(  # redirect to gallery index
            url_for('gallery.index')
        )

    if request.method == 'POST':  # if form is submitted
        db.session.delete(gallery)
        db.session.commit()

        flash(  # flash message
            'Gallery deleted',
            'success'
        )

        return redirect(  # redirect to gallery index
            url_for('gallery.index')
        )

    return render_template(  # render delete gallery form
        'gallery/gallery/delete.html',  # template
        gallery=gallery,  # gallery
        title='Delete Gallery'  # title
    )


@bp.route('/gallery-<gallery_id>/new-album', methods=['GET', 'POST'])
@login_required
def c_album(gallery_id):
    """
    Create album

    :param gallery_id: gallery id

    :return: new album form
    """
    gallery = Gallery.get_gallery(gallery_id)  # get gallery

    if not gallery:  # if gallery not found

        flash(  # flash message
            'Gallery not found',
            'danger'
        )
        return redirect(  # redirect to gallery index
            url_for('gallery.index')
        )

    form = AlbumForm()  # create form instance

    if form.validate_on_submit():  # if form is submitted

        album = Album(  # create album
            name=form.name.data,  # title
            description=form.description.data,  # description
            gallery_id=gallery_id  # gallery id
        )

        db.session.add(album)  # add album
        db.session.commit()  # commit changes

        flash(  # flash message
            'Album created',
            'success'
        )

        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_id=gallery_id)
        )

    return render_template(  # render new album form
        'gallery/album/form.html',  # template
        gallery=gallery,  # gallery
        form=form,  # form
        title='New Album'  # title
    )


@bp.route('/gallery-<gallery_id>/album-<album_id>')
def r_album(gallery_id, album_id):
    """
    Read album/Images index

    :param gallery_id: gallery id
    :param album_id: album id

    :return: album
    """
    album = Album.get_album(album_id)  # get album

    if not album:  # if album not found
        flash(  # flash message
            'Album not found',
            'danger'
        )
        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_id=gallery_id
            )
        )

    gallery = Gallery.get_gallery(album.gallery_id)  # get gallery

    return render_template(  # render album
        'gallery/album/index.html',  # template
        album=album,  # album
        gallery=gallery,  # gallery
        title=album.name  # title
    )


@bp.route('/gallery-<gallery_id>/album-<album_id>/edit', methods=['GET', 'POST'])
@login_required
def u_album(gallery_id, album_id):
    """
    Update album

    :param gallery_id: gallery id
    :param album_id: album id

    :return: edit album form
    """
    album = Album.get_album(album_id)  # get album

    if not album:  # if album not found
        flash(  # flash message
            'Album not found',
            'danger'
        )
        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_id=gallery_id
            )
        )

    gallery = Gallery.get_gallery(album.gallery_id)  # get gallery

    form = AlbumForm(obj=album)  # create form instance

    if form.validate_on_submit():  # if form is submitted, update album
        album.name = form.name.data
        album.description = form.description.data

        db.session.commit()  # commit changes

        flash(  # flash message
            'Album updated',
            'success'
        )

        return redirect(  # redirect to album
            url_for(
                'gallery.r_album',
                gallery_id=gallery_id,
                album_id=album_id
            )
        )

    return render_template(
        'gallery/album/form.html',  # template
        gallery=gallery,  # gallery
        album=album,  # album
        form=form,  # form
        title='Edit Album'  # title
    )


@bp.route('/gallery-<gallery_id>/album-<album_id>/delete', methods=['GET', 'POST'])
@login_required
def d_album(gallery_id, album_id):
    """
    Delete album

    :param gallery_id: gallery id
    :param album_id: album id

    :return: delete album
    """
    album = Album.get_album(album_id)  # get album

    if not album:  # if album not found
        flash(  # flash message
            'Album not found',
            'danger'
        )

        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_id=gallery_id
            )
        )

    gallery = Gallery.get_gallery(album.gallery_id)  # get gallery

    if request.method == 'POST':  # if form is submitted
        db.session.delete(album)
        db.session.commit()

        flash(  # flash message
            'Album deleted',
            'success'
        )

        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_id=gallery_id
            )
        )

    return render_template(  # render delete album form
        'gallery/album/delete.html',  # template
        gallery=gallery,  # gallery id
        album=album,  # album
        title='Delete Album'  # title
    )


@bp.route('/gallery-<gallery_id>/album-<album_id>/new-image', methods=['GET', 'POST'])
@login_required
def c_image(gallery_id, album_id):
    """
    Create image

    :param gallery_id: gallery id
    :param album_id: album id

    :return: new image form
    """
    return f'New image in gallery {gallery_id}, album {album_id}'


@bp.route('/gallery-<gallery_id>/album-<album_id>/image-<image_id>')
def r_image(gallery_id, album_id, image_id):
    """
    Read image

    :param gallery_id: gallery id
    :param album_id: album id
    :param image_id: image id

    :return: image
    """
    return f'Gallery {gallery_id}, Album {album_id}, Image {image_id}'


@bp.route('/gallery-<gallery_id>/album-<album_id>/image-<image_id>/edit', methods=['GET', 'POST'])
@login_required
def u_image(gallery_id, album_id, image_id):
    """
    Update image

    :param gallery_id: gallery id
    :param album_id: album id
    :param image_id: image id

    :return: edit image form
    """
    return f'Edit image {image_id} in gallery {gallery_id}, album {album_id}'


@bp.route('/gallery-<gallery_id>/album-<album_id>/image-<image_id>/delete', methods=['GET', 'POST'])
@login_required
def d_image(gallery_id, album_id, image_id):
    """
    Delete image

    :param gallery_id: gallery id
    :param album_id: album id
    :param image_id: image id

    :return: delete image
    """
    return f'Delete image {image_id} in gallery {gallery_id}, album {album_id}'
