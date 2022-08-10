from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

login_manager = LoginManager()

# SQLAlchemy Database Extension
db = SQLAlchemy()

# SQLAlchemy Migration Extension
migrate = Migrate()

# Flask Debug Toolbar
toolbar = DebugToolbarExtension()


def create_app(config="spar.config.TestConfig"):

    app = Flask(__name__)

    app.config.from_object(config)

    # Register Extenstions
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    # Import models
    import spar.models

    # Registers all blueprints
    from .settings import register_blueprints
    register_blueprints(app)

    return app