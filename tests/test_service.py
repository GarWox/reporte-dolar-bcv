from __future__ import annotations

from datetime import datetime, timezone

import pytest

import dolar_monitor.service as service
from dolar_monitor.config import Settings
from dolar_monitor.errors import SourceError
from dolar_monitor.models import BcvRates, BinanceRates

NOW = datetime(2026, 11, 13, 14, 30, tzinfo=timezone.utc)


def _boom(*args: object, **kwargs: object) -> None:
    raise SourceError("fuente caída")


def test_partial_failure_keeps_available_data(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "fetch_bcv", _boom)
    monkeypatch.setattr(
        service, "fetch_binance", lambda *args, **kwargs: BinanceRates(buy=40.25, sell=40.9)
    )

    snapshot = service.fetch_snapshot(settings, client=object(), now=NOW)  # type: ignore[arg-type]

    assert snapshot.bcv is None
    assert snapshot.binance == BinanceRates(buy=40.25, sell=40.9)
    assert snapshot.errors == ("fuente caída",)
    assert snapshot.has_data is True


def test_all_sources_failing(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "fetch_bcv", _boom)
    monkeypatch.setattr(service, "fetch_binance", _boom)

    snapshot = service.fetch_snapshot(settings, client=object(), now=NOW)  # type: ignore[arg-type]

    assert snapshot.has_data is False
    assert len(snapshot.errors) == 2
    assert snapshot.spread_buy is None


def test_successful_snapshot(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "fetch_bcv", lambda *args, **kwargs: BcvRates(36.5872, 42.1056))
    monkeypatch.setattr(
        service, "fetch_binance", lambda *args, **kwargs: BinanceRates(buy=40.25, sell=40.9)
    )

    snapshot = service.fetch_snapshot(settings, client=object(), now=NOW)  # type: ignore[arg-type]

    assert snapshot.errors == ()
    assert snapshot.spread_buy == 10.01
    assert snapshot.spread_sell == 11.79
