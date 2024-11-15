"""Flask application factory"""
from flask import Flask
from app.extensions import db
from app.views import routes
from config import Config


def create_app(config_class=Config):
    """Create a Flask application"""
    application = Flask(__name__)
    application.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(application)

    # pylint: disable=unused-import,import-outside-toplevel
    from app.models import image, album, gallery  # noqa: F401
    with application.app_context():
        db.create_all()

    # Register blueprints here
    application.register_blueprint(routes.bp)

    return application
