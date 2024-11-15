"""Gallery views"""
from flask import Blueprint, render_template, flash
from flask_login import login_required  # type: ignore
from app.forms.login import LoginForm
from app.controllers.gallery_controller import GalleryController
from app.controllers.user_controller import UserController

bp = Blueprint('gallery', __name__)


@bp.route('/')
def index():
    """Gallery index"""
    return render_template(
        'gallery/index.html',
        galleries=GalleryController.get_all_galleries()
    )


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    form = LoginForm()
    if form.validate_on_submit():
        user = UserController.user_login(form.email.data, form.password.data)
        if user:
            return 'Login successful'
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)


@bp.route('/new-gallery')
@login_required
def c_gallery():
    """Create gallery"""
    return 'New gallery'


@bp.route('/<gallery>')
def r_gallery(gallery):
    """Read gallery/Albums index"""
    return f'Gallery {gallery}'


@bp.route('/<gallery>/edit-gallery')
def u_gallery(gallery):
    """Update gallery"""
    return f'Edit gallery {gallery}'


@bp.route('/<gallery>/delete-gallery')
def d_gallery(gallery):
    """Delete gallery"""
    return f'Delete gallery {gallery}'


@bp.route('/<gallery>/new-album')
def c_album(gallery):
    """Create album"""
    return f'New album in gallery {gallery}'


@bp.route('/<gallery>/<album>')
def r_album(gallery, album):
    """Read album/Images index"""
    return f'Gallery {gallery}, Album {album}'


@bp.route('/<gallery>/<album>/edit-album')
def u_album(gallery, album):
    """Update album"""
    return f'Edit album {album} in gallery {gallery}'


@bp.route('/<gallery>/<album>/delete-album')
def d_album(gallery, album):
    """Delete album"""
    return f'Delete album {album} in gallery {gallery}'


@bp.route('/<gallery>/<album>/new-image')
def c_image(gallery, album):
    """Create image"""
    return f'New image in gallery {gallery}, album {album}'


@bp.route('/<gallery>/<album>/<image>')
def r_image(gallery, album, image):
    """Read image"""
    return f'Gallery {gallery}, Album {album}, Image {image}'


@bp.route('/<gallery>/<album>/<image>/edit-image')
def u_image(gallery, album, image):
    """Update image"""
    return f'Edit image {image} in gallery {gallery}, album {album}'


@bp.route('/<gallery>/<album>/<image>/delete-image')
def d_image(gallery, album, image):
    """Delete image"""
    return f'Delete image {image} in gallery {gallery}, album {album}'
