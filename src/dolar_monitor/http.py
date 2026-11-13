from __future__ import annotations

import logging

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.exceptions import SSLError as Urllib3SSLError
from urllib3.util.retry import Retry

from .config import Settings

logger = logging.getLogger(__name__)

USER_AGENT = "reporte-dolar-bcv/2.0 (+https://github.com/GarWox/reporte-dolar-bcv)"
RETRY_STATUSES = (429, 500, 502, 503, 504)


class _NoSslRetry(Retry):
    def increment(
        self,
        method=None,
        url=None,
        response=None,
        error=None,
        _pool=None,
        _stacktrace=None,
    ):
        if isinstance(error, Urllib3SSLError):
            raise error
        return super().increment(
            method,
            url,
            response=response,
            error=error,
            _pool=_pool,
            _stacktrace=_stacktrace,
        )



class HttpClient:
    def __init__(
        self,
        settings: Settings,
        retries: int = 3,
        session: requests.Session | None = None,
    ) -> None:
        self._timeout = settings.http_timeout
        self._session = session or requests.Session()
        retry = _NoSslRetry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=RETRY_STATUSES,
            allowed_methods=frozenset({"GET", "POST"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        self._session.headers.setdefault("User-Agent", USER_AGENT)

    def get(self, url: str) -> requests.Response:
        return self._request("GET", url)

    def post(self, url: str, **kwargs: object) -> requests.Response:
        return self._request("POST", url, **kwargs)

    def _request(self, method: str, url: str, **kwargs: object) -> requests.Response:
        kwargs.setdefault("timeout", self._timeout)
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.exceptions.SSLError:
            logger.warning("Fallo de verificación TLS en %s; reintentando sin verificar", url)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            kwargs["verify"] = False
            response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
