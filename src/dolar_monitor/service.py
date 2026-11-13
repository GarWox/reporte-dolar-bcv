from __future__ import annotations

from datetime import datetime, timezone

import requests

from .config import Settings
from .errors import SourceError
from .http import HttpClient
from .models import BcvRates, BinanceRates, Snapshot
from .sources.bcv import fetch_bcv
from .sources.binance import fetch_binance


def fetch_snapshot(
    settings: Settings,
    client: HttpClient | None = None,
    now: datetime | None = None,
) -> Snapshot:
    client = client or HttpClient(settings)
    errors: list[str] = []
    bcv: BcvRates | None = None
    binance: BinanceRates | None = None

    try:
        bcv = fetch_bcv(client, settings.bcv_url)
    except (SourceError, requests.RequestException) as exc:
        errors.append(str(exc))

    try:
        binance = fetch_binance(client, settings.binance_url)
    except (SourceError, requests.RequestException) as exc:
        errors.append(str(exc))

    return Snapshot(
        fetched_at=now or datetime.now(timezone.utc),
        bcv=bcv,
        binance=binance,
        errors=tuple(errors),
    )
