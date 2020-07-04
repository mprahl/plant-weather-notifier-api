# SPDX-License-Identifier: GPL-3.0-or-later
import abc

from plant_wn.weather.requests_utils import get_requests_session


class BaseWeatherAPI(abc.ABC):
    """The base class for all weather APIs."""

    def __init__(self, coordinates, api_key=None):
        """
        Initialize the WeatherAPI subclass.

        :param tuple(float, float) coordinates: a tuple where the first value is the longitude
            and the second value is the latitude.
        :param str api_key: an optional API key to use when getting the weather from an external
            service.
        """
        self.api_key = api_key
        self.coordinates = coordinates
        self.session = get_requests_session()

    @abc.abstractmethod
    def get_precipitation_forecast(self):
        """
        Get the daily precipitation accumulation forecast in inches.

        :return: a list of floats where the first index is today and each subsequent value is
            the following day. The floats are the precipitation accumulations.
        :rtype: list(float)
        :raises WeatherAPIError: if the forecast cannot be determined.
        """
        return  # pragma: no cover

    @abc.abstractmethod
    def get_temperature_forecast(self):
        """
        Get the daily temperature forecast in Fahrenheit.

        :return: a list of tuples where the first index is today and each subsequent value is
            the following day. The tuples will have the first value as the minimum temperature
            and the following day will be the maximum temperature.
        :rtype: list(tuple)
        :raises WeatherAPIError: if the forecast cannot be determined.
        """
        return  # pragma: no cover

    @abc.abstractmethod
    def get_wind_forecast(self):
        """
        Get the daily maximum wind forecast in miles per hour.

        :return: a list of floats where the first index is today and each subsequent value is
            the following day. The floats are the maximum wind speeds.
        :rtype: list(float)
        :raises WeatherAPIError: if the forecast cannot be determined.
        """
        return  # pragma: no cover
