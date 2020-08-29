# SPDX-License-Identifier: GPL-3.0-or-later
from unittest import mock

import pytest
from requests import RequestException

from plant_wn.exceptions import CoordinatesAPIError
from plant_wn.coordinates.opendatasoft import OpenDataSoftAPI


def test_get_coordinates():
    api = OpenDataSoftAPI("27601", api_key="some key")
    mock_session = mock.Mock()
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {
        "nhits": 1,
        "parameters": {
            "dataset": "us-zip-code-latitude-and-longitude",
            "timezone": "UTC",
            "q": "27601",
            "rows": 1,
            "format": "json",
        },
        "records": [
            {
                "datasetid": "us-zip-code-latitude-and-longitude",
                "recordid": "0334239674eb0135053d8022065a7ebcdee83ef2",
                "fields": {
                    "city": "Raleigh",
                    "zip": "27601",
                    "dst": 1,
                    "geopoint": [35.774451, -78.63274],
                    "longitude": -78.63274,
                    "state": "NC",
                    "latitude": 35.774451,
                    "timezone": -5,
                },
                "geometry": {"type": "Point", "coordinates": [-78.63274, 35.774451]},
                "record_timestamp": "2018-02-09T16:33:38.603000+00:00",
            }
        ],
    }
    api.session = mock_session

    assert api.get_coordinates() == (35.774451, -78.63274)


def test_get_coordinates_connection_error():
    api = OpenDataSoftAPI("27601", api_key="some key")
    mock_session = mock.Mock()
    mock_session.get.side_effect = RequestException()
    api.session = mock_session

    expected = "Failed to get the coordinates from the OpenDataSoft API"
    with pytest.raises(CoordinatesAPIError, match=expected):
        api.get_coordinates()


def test_get_coordinates_bad_status_code():
    api = OpenDataSoftAPI("27601", api_key="some key")
    mock_session = mock.Mock()
    mock_session.get.return_value.ok = False
    api.session = mock_session

    expected = "Failed to get the coordinates from the OpenDataSoft API"
    with pytest.raises(CoordinatesAPIError, match=expected):
        api.get_coordinates()


def test_get_coordinates_no_records():
    api = OpenDataSoftAPI("27601", api_key="some key")
    mock_session = mock.Mock()
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = {
        "nhits": 1,
        "parameters": {
            "dataset": "us-zip-code-latitude-and-longitude",
            "timezone": "UTC",
            "q": "27601",
            "rows": 1,
            "format": "json",
        },
        "records": [],
    }
    api.session = mock_session

    expected = "The coordinates for the zip code could not be found using the OpenDataSoft API"
    with pytest.raises(CoordinatesAPIError, match=expected):
        api.get_coordinates()
