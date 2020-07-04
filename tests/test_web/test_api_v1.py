# SPDX-License-Identifier: GPL-3.0-or-later
from unittest import mock


def test_get_plants(client):
    rv = client.get("/api/v1/plants")
    assert rv.status_code == 200
    assert rv.json == []


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
