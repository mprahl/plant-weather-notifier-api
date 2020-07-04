# SPDX-License-Identifier: GPL-3.0-or-later
from unittest import mock

import pytest
from requests import RequestException

from plant_wn.exceptions import WeatherAPIError
from plant_wn.weather.climacell import ClimaCellAPI


@pytest.fixture()
def climacell_forecast():
    return [
        {
            "temp": [
                {"observation_time": "2020-07-05T09:00:00Z", "min": {"value": 70.43, "units": "F"}},
                {"observation_time": "2020-07-04T18:00:00Z", "max": {"value": 94.02, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.0295, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-05T02:00:00Z",
                    "min": {"value": 2.15, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-05T03:00:00Z",
                    "max": {"value": 6.18, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-04"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-05T10:00:00Z", "min": {"value": 69.89, "units": "F"}},
                {"observation_time": "2020-07-05T20:00:00Z", "max": {"value": 90.95, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.4995, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-06T05:00:00Z",
                    "min": {"value": 1.36, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-05T23:00:00Z",
                    "max": {"value": 13.12, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-05"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-06T10:00:00Z", "min": {"value": 71.04, "units": "F"}},
                {"observation_time": "2020-07-06T18:00:00Z", "max": {"value": 92.95, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.0148, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-07T02:00:00Z",
                    "min": {"value": 2.59, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-06T21:00:00Z",
                    "max": {"value": 7.32, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-06"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-08T09:00:00Z", "min": {"value": 70.97, "units": "F"}},
                {"observation_time": "2020-07-07T20:00:00Z", "max": {"value": 91.49, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.0025, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-07T10:00:00Z",
                    "min": {"value": 3.37, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-08T00:00:00Z",
                    "max": {"value": 9.35, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-07"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-08T10:00:00Z", "min": {"value": 69.94, "units": "F"}},
                {"observation_time": "2020-07-08T17:00:00Z", "max": {"value": 85.19, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.4257, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-09T05:00:00Z",
                    "min": {"value": 3.81, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-09T02:00:00Z",
                    "max": {"value": 5.81, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-08"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-10T09:00:00Z", "min": {"value": 73.46, "units": "F"}},
                {"observation_time": "2020-07-09T18:00:00Z", "max": {"value": 85.22, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.1673, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-10T09:00:00Z",
                    "min": {"value": 4.58, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-09T21:00:00Z",
                    "max": {"value": 7.83, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-09"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-11T06:00:00Z", "min": {"value": 74.39, "units": "F"}},
                {"observation_time": "2020-07-10T18:00:00Z", "max": {"value": 81.61, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.2641, "units": "in"},
            "wind_speed": [
                {"observation_time": "2020-07-11T03:00:00Z", "min": {"value": 5.4, "units": "mph"}},
                {
                    "observation_time": "2020-07-10T21:00:00Z",
                    "max": {"value": 9.36, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-10"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-12T09:00:00Z", "min": {"value": 70.34, "units": "F"}},
                {"observation_time": "2020-07-11T18:00:00Z", "max": {"value": 83.93, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.2092, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-12T06:00:00Z",
                    "min": {"value": 2.76, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-11T18:00:00Z",
                    "max": {"value": 8.88, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-11"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-13T09:00:00Z", "min": {"value": 72.41, "units": "F"}},
                {"observation_time": "2020-07-12T21:00:00Z", "max": {"value": 88.43, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.0279, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-13T03:00:00Z",
                    "min": {"value": 1.76, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-12T18:00:00Z",
                    "max": {"value": 8.72, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-12"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-14T09:00:00Z", "min": {"value": 75.74, "units": "F"}},
                {"observation_time": "2020-07-13T18:00:00Z", "max": {"value": 98.57, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-13T15:00:00Z",
                    "min": {"value": 1.51, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-14T06:00:00Z",
                    "max": {"value": 6.83, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-13"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-15T09:00:00Z", "min": {"value": 77.5, "units": "F"}},
                {
                    "observation_time": "2020-07-14T21:00:00Z",
                    "max": {"value": 100.31, "units": "F"},
                },
            ],
            "precipitation_accumulation": {"value": 0, "units": "in"},
            "wind_speed": [
                {"observation_time": "2020-07-14T21:00:00Z", "min": {"value": 6.4, "units": "mph"}},
                {
                    "observation_time": "2020-07-15T03:00:00Z",
                    "max": {"value": 9.76, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-14"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-16T09:00:00Z", "min": {"value": 76.55, "units": "F"}},
                {"observation_time": "2020-07-15T18:00:00Z", "max": {"value": 98.46, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-16T09:00:00Z",
                    "min": {"value": 5.54, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-15T21:00:00Z",
                    "max": {"value": 8.46, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-15"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-17T09:00:00Z", "min": {"value": 76.19, "units": "F"}},
                {"observation_time": "2020-07-16T18:00:00Z", "max": {"value": 94.91, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-17T09:00:00Z",
                    "min": {"value": 5.72, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-16T21:00:00Z",
                    "max": {"value": 9.56, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-16"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-18T09:00:00Z", "min": {"value": 74.03, "units": "F"}},
                {"observation_time": "2020-07-17T18:00:00Z", "max": {"value": 95.63, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.0262, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-17T15:00:00Z",
                    "min": {"value": 5.94, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-18T03:00:00Z",
                    "max": {"value": 9.04, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-17"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
        {
            "temp": [
                {"observation_time": "2020-07-19T09:00:00Z", "min": {"value": 73, "units": "F"}},
                {"observation_time": "2020-07-18T21:00:00Z", "max": {"value": 95, "units": "F"}},
            ],
            "precipitation_accumulation": {"value": 0.0443, "units": "in"},
            "wind_speed": [
                {
                    "observation_time": "2020-07-19T03:00:00Z",
                    "min": {"value": 1.41, "units": "mph"},
                },
                {
                    "observation_time": "2020-07-19T00:00:00Z",
                    "max": {"value": 12.17, "units": "mph"},
                },
            ],
            "observation_time": {"value": "2020-07-18"},
            "lat": 35.7757,
            "lon": -78.6363,
        },
    ]


def test_forecast(climacell_forecast):
    api = ClimaCellAPI((35.7757, -78.6363), api_key="some_key")
    mock_session = mock.Mock()
    mock_session.get.return_value.ok = True
    mock_session.get.return_value.json.return_value = climacell_forecast
    api.session = mock_session

    assert not hasattr(api, "_forecast")
    assert api.forecast == climacell_forecast
    mock_session.get.assert_called_once_with(
        "https://api.climacell.co/v3/weather/forecast/daily",
        headers={"Content-Type": "application/json", "apikey": "some_key"},
        params={
            "lat": 35.7757,
            "lon": -78.6363,
            "unit_system": "us",
            "fields": ["precipitation_accumulation", "temp", "wind_speed"],
        },
        timeout=30,
    )


def test_forecast_connection_error():
    api = ClimaCellAPI((35.7757, -78.6363), api_key="some_key")
    mock_session = mock.Mock()
    mock_session.get.side_effect = RequestException()
    api.session = mock_session

    expected = "Failed to get the daily forecast from the ClimaCell API"
    with pytest.raises(WeatherAPIError, match=expected):
        api.forecast


def test_forecast_bad_status_code():
    api = ClimaCellAPI((35.7757, -78.6363), api_key="some_key")
    mock_session = mock.Mock()
    mock_session.get.return_value.ok = False
    api.session = mock_session

    expected = "Failed to get the daily forecast from the ClimaCell API"
    with pytest.raises(WeatherAPIError, match=expected):
        api.forecast


def test_get_precipitation_forecast(climacell_forecast):
    api = ClimaCellAPI((35.7757, -78.6363), api_key="some_key")
    api._forecast = climacell_forecast

    assert api.get_precipitation_forecast() == [
        0.0295,
        0.4995,
        0.0148,
        0.0025,
        0.4257,
        0.1673,
        0.2641,
        0.2092,
        0.0279,
        0,
        0,
        0,
        0,
        0.0262,
        0.0443,
    ]


def test_get_temperature_forecast(climacell_forecast):
    api = ClimaCellAPI((35.7757, -78.6363), api_key="some_key")
    api._forecast = climacell_forecast

    assert api.get_temperature_forecast() == [
        (70.43, 94.02),
        (69.89, 90.95),
        (71.04, 92.95),
        (70.97, 91.49),
        (69.94, 85.19),
        (73.46, 85.22),
        (74.39, 81.61),
        (70.34, 83.93),
        (72.41, 88.43),
        (75.74, 98.57),
        (77.5, 100.31),
        (76.55, 98.46),
        (76.19, 94.91),
        (74.03, 95.63),
        (73, 95),
    ]


def test_get_wind_forecast(climacell_forecast):
    api = ClimaCellAPI((35.7757, -78.6363), api_key="some_key")
    api._forecast = climacell_forecast

    assert api.get_wind_forecast() == [
        6.18,
        13.12,
        7.32,
        9.35,
        5.81,
        7.83,
        9.36,
        8.88,
        8.72,
        6.83,
        9.76,
        8.46,
        9.56,
        9.04,
        12.17,
    ]
