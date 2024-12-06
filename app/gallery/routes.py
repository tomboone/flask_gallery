"""
Gallery routes
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required  # type: ignore
from slugify import slugify  # type: ignore
from app.extensions import db
from app.forms.album_form import AlbumForm
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
            name=form.name.data,
            slug=slugify(form.name.data),
            description=form.description.data
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


@bp.route('/<gallery_slug>')
def r_gallery(gallery_slug):
    """
    Read gallery/Albums index

    :param gallery_slug: gallery slug

    :return: gallery
    """
    gallery = Gallery.get_gallery_by_slug(gallery_slug)  # get gallery

    if gallery is None:  # if gallery not found

        abort(404)  # abort

    return render_template(  # render gallery
        'gallery/gallery/index.html',  # template
        gallery=gallery,  # gallery
        title=gallery.name  # title
    )


@bp.route('/<gallery_slug>/edit')
@login_required
def u_gallery(gallery_slug):
    """
    Update gallery

    :param gallery_slug: gallery slug

    :return: edit gallery form
    """
    gallery = Gallery.get_gallery_by_slug(gallery_slug)  # get gallery

    if gallery is None:  # if gallery not found

        abort(404)  # abort

    form = GalleryForm(obj=gallery)  # create form instance

    if form.validate_on_submit():  # if form is submitted, update gallery

        gallery.name = form.name.data  # name
        gallery.slug = slugify(form.name.data)  # slug
        gallery.description = form.description.data  # description

        db.session.commit()  # commit changes

        flash(  # flash message
            'Gallery updated',
            'success'
        )

        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_slug=gallery_slug
            )
        )

    return render_template(  # render edit gallery form
        'gallery/gallery/form.html',  # template
        gallery=gallery,  # gallery
        form=form,  # form
        title='Edit Gallery'  # title
    )


@bp.route('/<gallery_slug>/delete', methods=['GET', 'POST'])
@login_required
def d_gallery(gallery_slug):
    """
    Delete gallery

    :param gallery_slug: gallery slug

    :return: delete gallery
    """
    gallery = Gallery.get_gallery_by_slug(gallery_slug)  # get gallery

    if gallery is None:  # if gallery not found

        abort(404)  # abort

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


@bp.route('/<gallery_slug>/new-album', methods=['GET', 'POST'])
@login_required
def c_album(gallery_slug):
    """
    Create album

    :param gallery_slug: gallery slug

    :return: new album form
    """
    gallery = Gallery.get_gallery_by_slug(gallery_slug)  # get gallery

    if gallery is None:  # if gallery not found

        abort(404)  # abort

    form = AlbumForm()  # create form instance

    if form.validate_on_submit():  # if form is submitted

        album = Album(  # create album
            name=form.name.data,  # title
            slug=slugify(form.name.data),  # slug
            description=form.description.data,  # description
            gallery_id=gallery.id  # gallery id
        )

        db.session.add(album)  # add album
        db.session.commit()  # commit changes

        flash(  # flash message
            'Album created',
            'success'
        )

        return redirect(  # redirect to album
            url_for(
                'gallery.r_album',
                album_slug=album.slug)
        )

    return render_template(  # render new album form
        'gallery/album/form.html',  # template
        gallery=gallery,  # gallery
        form=form,  # form
        title='New Album'  # title
    )


@bp.route('/<gallery_slug>/<album_slug>')
def r_album(gallery_slug, album_slug):
    """
    Read album/Images index

    :param gallery_slug: gallery slug
    :param album_slug: album slug

    :return: album
    """
    album = Album.get_album_by_slug(album_slug)  # get album
    gallery = Gallery.get_gallery(gallery_slug)  # get gallery

    if (  # if...
            gallery is None or  # ...gallery is None
            album is None or  # ...album is None
            album.gallery_id != gallery.id  # ...album does not belong to gallery
    ):
        abort(404)  # abort

    return render_template(  # render album
        'gallery/album/index.html',  # template
        album=album,  # album
        gallery=gallery,  # gallery
        title=album.name  # title
    )


@bp.route('/<gallery_slug>/<album_slug>/edit', methods=['GET', 'POST'])
@login_required
def u_album(gallery_slug, album_slug):
    """
    Update album

    :param gallery_slug: gallery slug
    :param album_slug: album slug

    :return: edit album form
    """
    album = Album.get_album_by_slug(album_slug)  # get album

    gallery = Gallery.get_gallery_by_slug(gallery_slug)  # get gallery

    if (  # if...
            album is None or   # ...album is None
            gallery is None or  # ...gallery is None
            album.gallery_id != gallery.id  # ...album does not belong to gallery
    ):
        abort(404)  # abort

    form = AlbumForm(obj=album)  # create form instance

    if form.validate_on_submit():  # if form is submitted, update album

        album.name = form.name.data  # name
        album.slug = slugify(form.name.data)  # slug
        album.description = form.description.data  # description

        db.session.commit()  # commit changes

        flash(  # flash message
            'Album updated',
            'success'
        )

        return redirect(  # redirect to album
            url_for(
                'gallery.r_album',
                gallery_slug=gallery_slug,
                album_slug=album_slug
            )
        )

    return render_template(
        'gallery/album/form.html',  # template
        gallery=gallery,  # gallery
        album=album,  # album
        form=form,  # form
        title='Edit Album'  # title
    )


@bp.route('/<gallery_slug>/<album_slug>/delete', methods=['GET', 'POST'])
@login_required
def d_album(gallery_slug, album_slug):
    """
    Delete album

    :param gallery_slug: gallery slug
    :param album_slug: album slug

    :return: delete album
    """
    album = Album.get_album_by_slug(album_slug)  # get album

    gallery = Gallery.get_gallery_by_slug(gallery_slug)  # get gallery

    if (  # if...
            album is None or  # ...album is None
            gallery is None or  # ...gallery is None
            album.gallery_id != gallery.id  # ...album does not belong to gallery
    ):
        abort(404)  # abort

    if request.method == 'POST':  # if form is submitted

        db.session.delete(album)  # delete album
        db.session.commit()  # commit changes

        flash(  # flash message
            'Album deleted',
            'success'
        )

        return redirect(  # redirect to gallery
            url_for(
                'gallery.r_gallery',
                gallery_slug=gallery_slug
            )
        )

    return render_template(  # render delete album form
        'gallery/album/delete.html',  # template
        gallery=gallery,  # gallery id
        album=album,  # album
        title='Delete Album'  # title
    )


@bp.route('/<gallery_slug>/<album_slug>/new-image', methods=['GET', 'POST'])
@login_required
def c_image(gallery_slug, album_slug):
    """
    Create image

    :param gallery_slug: gallery slug
    :param album_slug: album slug

    :return: new image form
    """
    return f'New image in gallery {gallery_slug}, album {album_slug}'


@bp.route('/<gallery_slug>/<album_slug>/<file_name>')
def r_image(gallery_slug, album_slug, file_name):
    """
    Read image

    :param gallery_slug: gallery slug
    :param album_slug: album slug
    :param file_name: file name

    :return: image
    """
    return f'Gallery {gallery_slug}, Album {album_slug}, Image {file_name}'


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
