from __future__ import annotations

from pathlib import Path

import pytest
import requests
import responses

from dolar_monitor.config import Settings
from dolar_monitor.errors import SourceError
from dolar_monitor.http import HttpClient
from dolar_monitor.sources.bcv import fetch_bcv, parse_bcv

FIXTURES = Path(__file__).parent / "fixtures"
BCV_HTML = (FIXTURES / "bcv.html").read_text(encoding="utf-8")


def test_parse_bcv_reads_usd_and_eur() -> None:
    rates = parse_bcv(BCV_HTML)

    assert rates.usd == 36.5872
    assert rates.eur == 42.1056


def test_parse_bcv_accepts_alternative_ids() -> None:
    html = (
        '<div id="dolar-ref"><strong>40,00</strong></div>'
        '<div id="euro-ref"><strong>44,00</strong></div>'
    )

    rates = parse_bcv(html)

    assert rates.usd == 40.0
    assert rates.eur == 44.0


def test_parse_bcv_raises_when_missing() -> None:
    with pytest.raises(SourceError):
        parse_bcv("<html><body></body></html>")


@responses.activate
def test_fetch_bcv(settings: Settings) -> None:
    responses.get(settings.bcv_url, body=BCV_HTML)

    rates = fetch_bcv(HttpClient(settings, retries=0), settings.bcv_url)

    assert rates.usd == 36.5872


@responses.activate
def test_fetch_bcv_wraps_http_errors(settings: Settings) -> None:
    responses.get(settings.bcv_url, status=503)

    with pytest.raises(SourceError, match="BCV no respondió"):
        fetch_bcv(HttpClient(settings, retries=0), settings.bcv_url)


@responses.activate
def test_fetch_bcv_falls_back_without_tls_verification(settings: Settings) -> None:
    def fail_tls(request: requests.PreparedRequest) -> None:
        raise requests.exceptions.SSLError("certificado inválido")

    responses.add_callback(responses.GET, settings.bcv_url, callback=fail_tls)
    responses.get(settings.bcv_url, body=BCV_HTML)

    rates = fetch_bcv(HttpClient(settings, retries=0), settings.bcv_url)

    assert rates.usd == 36.5872
    assert responses.calls[0].request.url == settings.bcv_url
    assert responses.calls[1].request.url == settings.bcv_url
