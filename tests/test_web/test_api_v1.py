# SPDX-License-Identifier: GPL-3.0-or-later
from unittest import mock

import bcrypt
import pytest

from plant_wn.web import models


def test_get_plants(client, user_token):
    rv = client.get("/api/v1/plants", headers={"Authorization": f"Bearer {user_token}"})
    assert rv.status_code == 200
    assert rv.json == []


def test_get_plants_unauthorized(client, user_token):
    rv = client.get("/api/v1/plants", headers={"Authorization": "Bearer ursine"})
    assert rv.status_code != 200


def test_healthcheck(client):
    rv = client.get("/api/v1/healthcheck")
    assert rv.status_code == 200
    assert rv.json == {"status": "Health check OK"}


@mock.patch("plant_wn.web.api_v1.db.engine.execute")
def test_healthcheck_failure(mock_db_execute, client):
    mock_db_execute.side_effect = RuntimeError()
    rv = client.get("/api/v1/healthcheck")
    assert rv.status_code == 500
    assert rv.json == {"error": "Database health check failed"}


def test_login(client, user):
    input_json = {"password": "Who's scruffy looking?", "username": "han_solo"}
    rv = client.post("/api/v1/login", json=input_json)
    assert rv.status_code == 200
    assert rv.json.get("token")


@pytest.mark.parametrize(
    "password, username",
    (("Don't everybody thank me at once", "han_solo"), ("Who's scruffy looking?", "yoda")),
)
def test_login_failed(password, username, client, user):
    rv = client.post("/api/v1/login", json={"password": password, "username": username})
    assert rv.status_code == 401
    assert rv.json == {"error": "The username or password was incorrect. Please try again."}


def test_new_user(client, db):
    input_password = "Who's scruffy looking?"
    input_username = "han_solo"
    rv = client.post("/api/v1/users", json={"password": input_password, "username": input_username})

    assert rv.status_code == 201
    assert rv.json == {"username": "han_solo"}
    user = db.session.query(models.User).filter_by(username=input_username).one()
    assert user.password != input_password
    assert bcrypt.checkpw(input_password.encode("utf-8"), user.password)
    assert user.username == input_username


@pytest.mark.parametrize(
    "json_input",
    (
        {"username": "han_solo"},
        {"password": "Who's scruffy looking?"},
        "han_solo",
        {"password": 123, "username": "han_solo"},
    ),
)
def test_new_user_invalid(json_input, client):
    rv = client.post("/api/v1/users", json=json_input)
    assert rv.status_code == 400
    expected = (
        "The input JSON must only contain the following keys with string values: password and "
        "username"
    )
    assert rv.json == {"error": expected}


def test_new_user_already_exists(client):
    json_input = {"password": "Who's scruffy looking?", "username": "han_solo"}
    rv = client.post("/api/v1/users", json=json_input)
    assert rv.status_code == 201
    rv = client.post("/api/v1/users", json=json_input)
    assert rv.status_code == 400
    assert rv.json == {"error": 'The user "han_solo" already exists'}


def test_not_found(client):
    rv = client.get("/api/v1/droids")
    assert rv.status_code == 404
    assert rv.json == {"error": "The requested resource was not found"}
