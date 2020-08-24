# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import os

from flask import Flask, jsonify
from flask.logging import default_handler
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import default_exceptions, HTTPException

from plant_wn.exceptions import AppError, ConfigError, ValidationError
from plant_wn.web import db
from plant_wn.web.api_v1 import api_v1

# Import the models here so that Alembic will be guaranteed to detect them
import plant_wn.web.models  # noqa: F401


def load_config(app):  # pragma: no cover
    """
    Determine the correct configuration to use and apply it.

    :param flask.Flask app: a Flask application object
    """
    config_file = None
    if app.config["ENV"] == "development":
        default_config_obj = "plant_wn.web.config.DevelopmentConfig"
    else:
        default_config_obj = "plant_wn.web.config.ProductionConfig"
        config_file = "/etc/plant_wn/settings.py"
    app.config.from_object(default_config_obj)

    if config_file and os.path.isfile(config_file):
        app.config.from_pyfile(config_file)


def validate_api_config(config):
    """
    Determine if the configuration is valid.

    :param dict config: the dict containing the plant_wn config
    :raises ConfigError: if the config is invalid
    """
    if config["ENV"] != "development" and config["SECRET_KEY"] == "change-me":
        raise ConfigError("SECRET_KEY cannot use the default value in production")


def create_app(config_obj=None):  # pragma: no cover
    """
    Create a Flask application object.

    :param str config_obj: the path to the configuration object to use instead of calling
        load_config
    :return: a Flask application object
    :rtype: flask.Flask
    """
    app = Flask("plant_wn")
    if config_obj:
        app.config.from_object(config_obj)
    else:
        load_config(app)
        # Validate the config
        validate_api_config(app.config)

    # Configure logging
    default_handler.setFormatter(
        logging.Formatter(fmt=app.config["PLANT_WN_LOG_FORMAT"], datefmt="%Y-%m-%d %H:%M:%S")
    )
    app.logger.setLevel(app.config["PLANT_WN_LOG_LEVEL"])
    for logger_name in app.config["PLANT_WN_ADDITIONAL_LOGGERS"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(app.config["PLANT_WN_LOG_LEVEL"])
        # Add the Flask handler that streams to WSGI stderr
        logger.addHandler(default_handler)

    # Initialize the database
    db.init_app(app)
    # Initialize the database migrations
    migrations_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "migrations")
    Migrate(app, db, directory=migrations_dir)
    # Initialize JSON web token support
    JWTManager(app)

    app.register_blueprint(api_v1, url_prefix="/api/v1")
    for code in default_exceptions.keys():
        app.register_error_handler(code, json_error)
    app.register_error_handler(AppError, json_error)

    return app


def json_error(error):
    """
    Convert exceptions to JSON responses.

    :param Exception error: an Exception to convert to JSON
    :return: a Flask JSON response
    :rtype: flask.Response
    """
    if isinstance(error, HTTPException):
        if error.code == 404:
            msg = "The requested resource was not found"
        else:
            msg = error.description
        response = jsonify({"error": msg})
        response.status_code = error.code
    else:
        status_code = 500
        msg = str(error)
        if isinstance(error, ValidationError):
            status_code = 400

        response = jsonify({"error": msg})
        response.status_code = status_code
    return response
