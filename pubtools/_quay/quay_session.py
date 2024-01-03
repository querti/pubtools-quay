from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# pylint: disable=bad-option-value,useless-object-inheritance
class QuaySession(object):
    """Helper class to support Quay requests and authentication."""

    def __init__(
        self,
        hostname: str | None = None,
        retries: int = 3,
        backoff_factor: int = 2,
        verify: bool = False,
        api: str = "docker",
    ) -> None:
        """
        Initialize.

        Args:
            hostname (str)
                hostname of Quay service.
            retries (int)
                number of http retries.
            backoff_factor (int)
                backoff factor to apply between attempts after the second try.
            verify (bool)
                enable/disable SSL CA verification.
            api (str):
                Which API queries to construct. Supported values: 'docker', 'quay'
        """
        if api not in ("docker", "quay"):
            raise ValueError("Unknown API type: '{0}'".format(api))
        self.api = api

        self.session = requests.Session()
        self.hostname = hostname or "quay.io"
        self.session.verify = verify
        self.session.headers["Host"] = self.hostname

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=set(range(500, 512)),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """
        HTTP GET request against Quay server API.

        Args:
            endpoint (str):
                Endpoint of the request.
            kwargs:
                Additional arguments to add to the requests method.
        Returns:
            requests.Response: A response object.
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
        return self.session.get(self._api_url(endpoint), **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """
        HTTP POST request against Quay server API.

        Args:
            endpoint (str):
                Endpoint of the request.
            kwargs:
                Additional arguments to add to the requests method.
        Returns:
            requests.Response: A response object.
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
        return self.session.post(self._api_url(endpoint), **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """
        HTTP PUT request against Quay server API.

        Args:
            endpoint (str):
                Endpoint of the request.
            kwargs:
                Additional arguments to add to the requests method.
        Returns:
            requests.Response: A response object.
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
        return self.session.put(self._api_url(endpoint), **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """
        HTTP DELETE request against Quay server API.

        Args:
            endpoint (str):
                Endpoint of the request.
            kwargs:
                Additional arguments to add to the requests method.
        Returns:
            requests.Response: A response object.
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
        return self.session.delete(self._api_url(endpoint), **kwargs)

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """
        HTTP generic request against Quay server API.

        Args:
            method (str):
                REST API method of the request (GET, POST, PUT, DELETE).
            endpoint (str):
                Endpoint of the request.
            kwargs:
                Additional arguments to add to the requests method.
        Returns:
            requests.Response: A response object.
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
        return self.session.request(method, self._api_url(endpoint), **kwargs)

    def _api_url(self, endpoint: str) -> str:
        """
        Generate full url of the API endpoint.

        Args:
            endpoint (str)
                API specific endpoint for the request.
        Returns:
            str: Full URL of the endpoint.
        """
        if self.api == "docker":
            schema = "{0}{1}/v2/{2}"
        elif self.api == "quay":
            schema = "{0}{1}/api/v1/{2}"

        if "http://" not in self.hostname and "https://" not in self.hostname:
            return schema.format("https://", self.hostname.rstrip("/"), endpoint)
        else:
            return schema.format("", self.hostname.rstrip("/"), endpoint)

    def set_auth_token(self, token: str) -> None:
        """
        Set a Bearer auth token for the authentication.

        Args:
            token (str):
                Bearer token.
        """
        self.session.headers["Authorization"] = "Bearer {0}".format(token)
