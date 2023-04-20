import os
import secrets

BASEDIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", False
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL")
    FLASK_APP = "wsgi.py"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DB_URL", "sqlite:///{}".format(os.path.join(BASEDIR, "project.db"))
    )


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DB_URL", "sqlite:///{}".format(os.path.join(BASEDIR, "project.db"))
    )