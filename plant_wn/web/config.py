# SPDX-License-Identifier: GPL-3.0-or-later
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
DEV_DB_FILE = os.path.join(BASE_DIR, "plant_wn.db")
TEST_DB_FILE = os.path.join(BASE_DIR, "plant_wn_test.db")


class Config(object):
    """The base plant_wn Flask configuration."""

    JWT_ERROR_MESSAGE_KEY = "error"
    # Claim in the tokens that is used as the source of identity. sub is used due to the JWT RFC.
    JWT_IDENTITY_CLAIM = "sub"
    # Additional loggers to set to the level defined in PLANT_WN_LOG_LEVEL
    PLANT_WN_ADDITIONAL_LOGGERS = []
    PLANT_WN_LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(module)s.%(funcName)s %(message)s"
    # This sets the level of the "flask.app" logger, which is accessed from current_app.logger
    PLANT_WN_LOG_LEVEL = "INFO"
    SECRET_KEY = "change-me"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """The production plant_wn Flask configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////etc/plant_wn.db"


class DevelopmentConfig(Config):
    """The development plant_wn Flask configuration."""

    PLANT_WN_LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DEV_DB_FILE}"


class TestingConfig(DevelopmentConfig):
    """The testing plant_wn Flask configuration."""

    DEBUG = True
    # IMPORTANT: don't use in-memory sqlite. Alembic migrations will create a new
    # connection producing a new instance of the database which is deleted immediately
    # after the migration completes...
    #   https://github.com/miguelgrinberg/Flask-Migrate/issues/153
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{TEST_DB_FILE}"
    LOGIN_DISABLED = False


class TestingConfigNoAuth(TestingConfig):
    """The testing PLANT_WN Flask configuration without authentication."""
