"""
Login routes
"""
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required, logout_user  # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.forms.login_form import LoginForm
from app.forms.user_form import UserForm
from app.models.user import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def index():
    """
    User index

    :return: redirect to user profile
    """
    return redirect(  # redirect to user profile
        url_for('user.profile')
    )


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    User profile

    :return: user profile
    """
    user = User.get_user(current_user.id)  # get current user

    form = UserForm(obj=user)  # create form instance with user data

    if form.validate_on_submit():  # if form is submitted

        user.email = form.email.data  # update email

        if form.new_password.data:  # if new password is provided

            if check_password_hash(user.password, form.current_password.data) is False:  # If current password wrong
                flash(  # flash error message
                    'Current password is incorrect',
                    'error'
                )

                return redirect(  # redirect back to user profile
                    url_for('user.profile', user_id=current_user.id)
                )

            if form.new_password.data != form.confirm_password.data:  # if new passwords don't match

                flash(  # flash error message
                    'New passwords don\'t match',
                    'error'
                )

                return redirect(  # redirect back to user profile
                    url_for('user.profile', user_id=current_user.id)
                )

            user.password = generate_password_hash(form.new_password.data)  # set new password

        db.session.commit()  # commit changes

        flash(  # flash message
            'User updated',
            'success'
        )
        return redirect(  # redirect back to user profile
            url_for('user.profile', user_id=current_user.id)
        )
    return render_template(  # render user profile form
        'user/form.html',
        user=current_user,  # user
        form=form,
        title='Profile'
    )


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page

    :return: login page
    """
    if current_user.is_authenticated:  # if user is authenticated
        return redirect(  # redirect to user profile
            url_for('user.profile', user_id=current_user.id)
        )

    form = LoginForm()  # create form instance

    if form.validate_on_submit():  # if form is submitted

        user = User.user_login(form.email.data, form.password.data)  # login user

        if user:  # if user is logged in

            flash(  # flash message
                'Login successful',
                'success'
            )
            return redirect(  # redirect to gallery index
                url_for('gallery.index')
            )

        flash(  # if login fails, flash error message
            'Invalid email or password',
            'error'
        )
        return redirect(  # redirect to login page
            url_for('user.login')
        )

    return render_template(  # if form is not submitted, render login page
        'user/login.html',  # template
        form=form,  # form
        title='Login'  # title
    )


@bp.route('/logout')
def logout():
    """
    Logout

    :return: redirect to login page
    """
    logout_user()  # logout user

    return redirect(  # redirect to login page
        url_for('gallery.index')
    )
