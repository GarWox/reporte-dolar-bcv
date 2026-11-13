from __future__ import annotations

import pytest
from urllib3.exceptions import SSLError

from dolar_monitor.http import _NoSslRetry


def test_ssl_errors_are_not_retried() -> None:
    retry = _NoSslRetry(total=3)

    with pytest.raises(SSLError):
        retry.increment(error=SSLError("certificado inválido"))
