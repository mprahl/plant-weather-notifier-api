# SPDX-License-Identifier: GPL-3.0-or-later
import logging

from requests import RequestException

from plant_wn.exceptions import CoordinatesAPIError
from plant_wn.coordinates.base import BaseCoordinatesAPI

log = logging.getLogger(__name__)


class OpenDataSoftAPI(BaseCoordinatesAPI):
    def get_coordinates(self):
        """
        Get the coordinates for the zip code.

        :return: a tuple with the first index as the latitude and the second index as the longitude.
        :rtype: tuple(float, float)
        :raises CoordinatesAPIError: if the coordinates cannot be determined.
        """
        url = "https://public.opendatasoft.com/api/records/1.0/search/"
        headers = {"Content-Type": "application/json"}
        query_params = {
            "dataset": "us-zip-code-latitude-and-longitude",
            "q": self.zip_code,
            "rows": 1,
        }
        msg = "Failed to get the coordinates from the OpenDataSoft API"
        try:
            rv = self.session.get(url, headers=headers, params=query_params, timeout=30)
        except RequestException:
            log.exception(msg)
            raise CoordinatesAPIError(msg)

        if not rv.ok:
            log.error(
                "%s. The status code was %d. The text was %s.", msg, rv.status_code, rv.text,
            )
            raise CoordinatesAPIError(msg)

        if not rv.json()["records"]:
            msg = "The coordinates for the zip code could not be found using the OpenDataSoft API"
            log.error(msg)
            raise CoordinatesAPIError(msg)

        return tuple(rv.json()["records"][0]["fields"]["geopoint"])
