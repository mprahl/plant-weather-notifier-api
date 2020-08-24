# SPDX-License-Identifier: GPL-3.0-or-later
import os

from flask_jwt_extended import create_access_token
import flask_migrate
import pytest

from plant_wn.web import models
from plant_wn.web.app import create_app, db as _db
from plant_wn.web.config import TEST_DB_FILE


@pytest.fixture()
def app(request):
    """Return the Flask application."""
    app = create_app("plant_wn.web.config.TestingConfig")
    # Establish an application context before running the tests. This allows the use of
    # Flask-SQLAlchemy in the test setup.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture()
def client(app, db):
    """Return Flask application client for the pytest session."""
    return app.test_client()


@pytest.fixture()
def db(app, tmpdir):
    """Yield a DB with required app tables but with no records."""
    # Clear the database for each test to ensure tests are idempotent.
    try:
        os.remove(TEST_DB_FILE)
    except FileNotFoundError:
        pass

    with app.app_context():
        flask_migrate.upgrade()

    return _db


@pytest.fixture()
def user(db):
    """Create a user in the database and return the user object."""
    input_json = {"password": "Who's scruffy looking?", "username": "han_solo"}
    user = models.User.from_json(input_json)
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture()
def user_token(user):
    """Generate and return a JWT token for the user from the user fixture."""
    return create_access_token(identity="han_solo")
