from __future__ import annotations

import json
from pathlib import Path

import pytest
import responses

from dolar_monitor.config import Settings
from dolar_monitor.errors import SourceError
from dolar_monitor.http import HttpClient
from dolar_monitor.sources.binance import fetch_binance

FIXTURES = Path(__file__).parent / "fixtures"
BUY = json.loads((FIXTURES / "binance_buy.json").read_text(encoding="utf-8"))
SELL = json.loads((FIXTURES / "binance_sell.json").read_text(encoding="utf-8"))


@responses.activate
def test_fetch_binance_reads_buy_and_sell(settings: Settings) -> None:
    responses.post(settings.binance_url, json=BUY)
    responses.post(settings.binance_url, json=SELL)

    rates = fetch_binance(HttpClient(settings, retries=0), settings.binance_url)

    assert rates.buy == 40.25
    assert rates.sell == 40.9


@responses.activate
def test_fetch_binance_rejects_empty_offers(settings: Settings) -> None:
    responses.post(settings.binance_url, json={"data": []})

    with pytest.raises(SourceError, match="no devolvió anuncios"):
        fetch_binance(HttpClient(settings, retries=0), settings.binance_url)


@responses.activate
def test_fetch_binance_rejects_non_json(settings: Settings) -> None:
    responses.post(settings.binance_url, body="<html>bloqueado</html>")

    with pytest.raises(SourceError, match="no JSON"):
        fetch_binance(HttpClient(settings, retries=0), settings.binance_url)


@responses.activate
def test_fetch_binance_rejects_unexpected_payload(settings: Settings) -> None:
    responses.post(settings.binance_url, json={"data": [{"adv": {}}]})

    with pytest.raises(SourceError, match="anuncio inesperado"):
        fetch_binance(HttpClient(settings, retries=0), settings.binance_url)
