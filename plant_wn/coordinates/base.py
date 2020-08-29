# SPDX-License-Identifier: GPL-3.0-or-later
import abc

from plant_wn.requests_utils import get_requests_session


class BaseCoordinatesAPI(abc.ABC):
    """The base class for all coordinates APIs."""

    def __init__(self, zip_code, api_key=None):
        """
        Initialize the BaseCoordinatesAPI subclass.

        :param str zip_code: the zip code to get the coordinates for.
        :param str api_key: an optional API key to use when getting the coordinates from an external
            service.
        """
        self.api_key = api_key
        self.zip_code = zip_code
        self.session = get_requests_session()

    @abc.abstractmethod
    def get_coordinates(self):
        """
        Get the coordinates for the zip code.

        :return: a tuple with the first index as the latitude and the second index as the longitude.
        :rtype: tuple(float, float)
        :raises CoordinatesAPIError: if the coordinates cannot be determined.
        """
        return  # pragma: no cover
