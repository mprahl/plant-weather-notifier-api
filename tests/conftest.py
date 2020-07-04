# SPDX-License-Identifier: GPL-3.0-or-later
import os

import flask_migrate
import pytest

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
def client(app):
    """Return Flask application client for the pytest session."""
    return app.test_client()
