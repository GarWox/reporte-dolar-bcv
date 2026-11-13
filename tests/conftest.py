from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from dolar_monitor.config import Settings
from dolar_monitor.models import BcvRates, BinanceRates, Snapshot

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def settings() -> Settings:
    return Settings(
        bcv_url="https://bcv.test/",
        binance_url="https://binance.test/p2p",
    )


@pytest.fixture
def snapshot() -> Snapshot:
    return Snapshot(
        fetched_at=datetime(2026, 11, 13, 14, 30, tzinfo=timezone.utc),
        bcv=BcvRates(usd=36.5872, eur=42.1056),
        binance=BinanceRates(buy=40.25, sell=40.9),
    )
