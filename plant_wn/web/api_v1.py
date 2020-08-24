# SPDX-License-Identifier: GPL-3.0-or-later
import flask
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.sql import text
from werkzeug.exceptions import Unauthorized

from plant_wn.web import models
from plant_wn.web.app import db
from plant_wn.exceptions import AppError

api_v1 = flask.Blueprint("api_v1", __name__)


@api_v1.route("/plants")
@jwt_required
def get_plants():
    """
    Retrieve the user's plants.

    :rtype: flask.Response
    """
    return flask.jsonify([])


@api_v1.route("/healthcheck")
def get_healthcheck():
    """
    Respond to a health check.

    :rtype: flask.Response
    :return: json object representing the health of the app
    :raises AppError: if the database connection fails
    """
    # Test DB connection
    try:
        db.engine.execute(text("SELECT 1"))
    except Exception:
        flask.current_app.logger.exception("The database test failed")
        raise AppError("Database health check failed")

    return flask.jsonify({"status": "Health check OK"})


@api_v1.route("/login", methods=["POST"])
def login():
    """
    Login the user.

    :rtype: flask.Response
    """
    json_input = flask.request.get_json(force=True)
    models.User.validate_json(json_input)
    user = db.session.query(models.User).filter_by(username=json_input["username"]).first()
    if not user:
        raise Unauthorized("The username or password was incorrect. Please try again.")

    user.validate_password(json_input["password"])
    access_token = create_access_token(identity=user.username)
    return flask.jsonify({"token": access_token})


@api_v1.route("/users", methods=["POST"])
def new_user():
    """
    Create a user.

    :rtype: tuple(flask.Response, int)
    """
    json_input = flask.request.get_json(force=True)
    user = models.User.from_json(json_input)
    db.session.add(user)
    db.session.commit()
    return flask.jsonify(user.to_json()), 201
