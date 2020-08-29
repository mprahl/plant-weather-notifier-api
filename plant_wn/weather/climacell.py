# SPDX-License-Identifier: GPL-3.0-or-later
import logging

from requests import RequestException

from plant_wn.exceptions import WeatherAPIError
from plant_wn.weather.base import BaseWeatherAPI

log = logging.getLogger(__name__)


class ClimaCellAPI(BaseWeatherAPI):
    """The ClimaCell weather API."""

    @property
    def forecast(self):
        """
        Get the forecast from the ClimaCell API.

        raises WeatherAPIError: if the forecast could not be determined.
        """
        if getattr(self, "_forecast", None) is None:
            url = "https://api.climacell.co/v3/weather/forecast/daily"
            headers = {"Content-Type": "application/json", "apikey": self.api_key}
            query_params = {
                "lat": self.coordinates[0],
                "lon": self.coordinates[1],
                "unit_system": "us",
                "fields": ["precipitation_accumulation", "temp", "wind_speed"],
            }
            msg = "Failed to get the daily forecast from the ClimaCell API"
            try:
                rv = self.session.get(url, headers=headers, params=query_params, timeout=30)
            except RequestException:
                log.exception(msg)
                raise WeatherAPIError(msg)

            if not rv.ok:
                log.error(
                    "%s. The status code was %d. The text was %s.", msg, rv.status_code, rv.text,
                )
                raise WeatherAPIError(msg)

            self._forecast = rv.json()

        return self._forecast

    def get_precipitation_forecast(self):
        """
        Get the daily precipitation accumulation forecast in inches.

        :return: a list of floats where the first index is today and each subsequent value is
            the following day. The floats are the precipitation accumulations.
        :rtype: list(float)
        :raises WeatherAPIError: if the forecast cannot be determined.
        """
        return [float(day["precipitation_accumulation"]["value"]) for day in self.forecast]

    def get_temperature_forecast(self):
        """
        Get the daily temperature forecast in Fahrenheit.

        :return: a list of tuples where the first index is today and each subsequent value is
            the following day. The tuples will have the first value as the minimum temperature
            and the following day will be the maximum temperature.
        :rtype: list(tuple)
        :raises WeatherAPIError: if the forecast cannot be determined.
        """
        return [
            (float(day["temp"][0]["min"]["value"]), float(day["temp"][1]["max"]["value"]))
            for day in self.forecast
        ]

    def get_wind_forecast(self):
        """
        Get the daily maximum wind forecast in miles per hour.

        :return: a list of floats where the first index is today and each subsequent value is
            the following day. The floats are the maximum wind speeds.
        :rtype: list(float)
        :raises WeatherAPIError: if the forecast cannot be determined.
        """
        return [float(day["wind_speed"][1]["max"]["value"]) for day in self.forecast]
