"""Flask application factory"""
import click
from flask import Flask, redirect, url_for, render_template
from flask.cli import FlaskGroup, with_appcontext
from app.extensions import db, login_manager
from config import Config


def create_app(config_class=Config) -> Flask:
    """Create a Flask application"""
    application = Flask(__name__)
    application.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(application)
    login_manager.init_app(application)

    # pylint: disable=unused-import,import-outside-toplevel
    from app.models import image, album, gallery, user  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id):
        """Load user
        """
        return db.session.execute(db.select(user.User).filter_by(id=user_id)).scalar_one_or_none()

    @login_manager.unauthorized_handler
    def unauthorized():
        """Unauthorized handler
        """
        return redirect(url_for('user.login'))

    # Register blueprints here
    from app.gallery import bp as gallery_bp
    application.register_blueprint(gallery_bp)

    from app.user import bp as user_bp
    application.register_blueprint(user_bp)

    application.cli.add_command(initdb)
    application.cli.add_command(createuser)

    @application.shell_context_processor
    def shell_context():
        """ Shell context """
        return {'app': application, 'db': db}

    @application.errorhandler(404)
    def page_not_found(e):
        """404 error handler
        """
        return render_template('404.html', e=e), 404

    return application


cli = FlaskGroup(create_app=create_app)


@cli.command(name='initdb')
@with_appcontext
def initdb():
    """Initialize the database
    """
    db.create_all()
    print('Database initialized')


@cli.command(name='createuser')
@click.option('-e', '--email', required=True, type=str)
@click.option('-p', '--password', required=True, type=str)
@with_appcontext
def createuser(email, password):
    """Create a user
    """
    from app.models.user import User  # pylint: disable=import-outside-toplevel
    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    print(f'User {user.email} created')
