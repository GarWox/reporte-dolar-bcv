from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from ..errors import SourceError
from ..http import HttpClient
from ..models import BcvRates
from ..parsing import parse_ves_number

DOLAR_IDS = ("dolar", "dolar-ref")
EURO_IDS = ("euro", "euro-ref")


def fetch_bcv(client: HttpClient, url: str) -> BcvRates:
    try:
        response = client.get(url)
    except requests.RequestException as exc:
        raise SourceError(f"BCV no respondió: {exc}") from exc
    return parse_bcv(response.text)


def parse_bcv(html: str) -> BcvRates:
    soup = BeautifulSoup(html, "html.parser")
    return BcvRates(
        usd=_extract_rate(soup, DOLAR_IDS, "USD"),
        eur=_extract_rate(soup, EURO_IDS, "EUR"),
    )


def _extract_rate(soup: BeautifulSoup, ids: tuple[str, ...], currency: str) -> float:
    for element_id in ids:
        container = soup.find(id=element_id)
        if container is None:
            continue
        strong = container.find("strong")
        if strong is None:
            continue
        try:
            value = parse_ves_number(strong.get_text(strip=True))
        except ValueError:
            continue
        if value > 0:
            return round(value, 4)
    raise SourceError(f"No se pudo extraer la tasa {currency} del BCV")
