from __future__ import annotations

import requests

from ..errors import SourceError
from ..http import HttpClient
from ..models import BinanceRates

ASSET = "USDT"
FIAT = "VES"


def fetch_binance(client: HttpClient, url: str) -> BinanceRates:
    return BinanceRates(
        buy=_fetch_price(client, url, "BUY"),
        sell=_fetch_price(client, url, "SELL"),
    )


def _fetch_price(client: HttpClient, url: str, trade_type: str) -> float:
    payload = {
        "asset": ASSET,
        "fiat": FIAT,
        "tradeType": trade_type,
        "page": 1,
        "rows": 1,
    }
    try:
        response = client.post(url, json=payload)
    except requests.RequestException as exc:
        raise SourceError(f"Binance P2P no respondió ({trade_type}): {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise SourceError(
            f"Binance P2P devolvió una respuesta no JSON ({trade_type})"
        ) from exc

    rows = data.get("data") if isinstance(data, dict) else None
    if not rows:
        raise SourceError(f"Binance P2P no devolvió anuncios para {trade_type}")

    try:
        price = float(rows[0]["adv"]["price"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise SourceError(
            f"Binance P2P devolvió un anuncio inesperado ({trade_type})"
        ) from exc

    if price <= 0:
        raise SourceError(f"Binance P2P devolvió un precio inválido ({trade_type})")
    return round(price, 4)
