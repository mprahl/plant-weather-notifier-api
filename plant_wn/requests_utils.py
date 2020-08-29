# SPDX-License-Identifier: GPL-3.0-or-later
import requests
from requests.packages.urllib3.util.retry import Retry


def get_requests_session():
    """
    Create a requests session with retries enabled.

    :return: the configured requests session
    :rtype: requests.Session
    """
    session = requests.Session()
    retry = Retry(
        total=3, read=3, connect=3, backoff_factor=1, status_forcelist=(500, 502, 503, 504)
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
