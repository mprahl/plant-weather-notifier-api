# SPDX-License-Identifier: GPL-3.0-or-later
import flask
from sqlalchemy.sql import text

from plant_wn.web.app import db
from plant_wn.exceptions import AppError

api_v1 = flask.Blueprint("api_v1", __name__)


@api_v1.route("/plants")
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
