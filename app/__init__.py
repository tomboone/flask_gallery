"""Flask application factory"""
import click
from flask import Flask
from flask.cli import FlaskGroup, with_appcontext
from app.extensions import db, login_manager
from app.controllers.user_controller import UserController
from app.views import routes
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

    with application.app_context():
        db.create_all()

    # Register blueprints here
    application.register_blueprint(routes.bp)

    application.cli.add_command(createuser)

    @application.shell_context_processor
    def shell_context():
        """ Shell context """
        return {'app': application, 'db': db}

    return application


cli = FlaskGroup(create_app=create_app)


@cli.command(name='createuser')
@click.option('-e', '--email', required=True, type=str)
@click.option('-p', '--password', required=True, type=str)
@with_appcontext
def createuser(email, password):
    """Create a user
    """
    user = UserController.create_user(email, password)
    db.session.add(user)
    db.session.commit()
    print(f'User {user.email} created')
