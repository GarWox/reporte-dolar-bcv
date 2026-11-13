from __future__ import annotations

from datetime import datetime, timezone

from dolar_monitor.models import Snapshot
from dolar_monitor.report import render_discord_embed, render_text

EMPTY = Snapshot(
    fetched_at=datetime(2026, 11, 13, 14, 30, tzinfo=timezone.utc),
    errors=("BCV no respondió: timeout",),
)


def test_render_text(snapshot: Snapshot) -> None:
    text = render_text(snapshot)

    assert "2026-11-13 14:30 UTC" in text
    assert "36.5872" in text
    assert "42.1056" in text
    assert "40.2500" in text
    assert "+10.01%" in text
    assert "+11.79%" in text
    assert "Advertencias" not in text


def test_render_text_without_data() -> None:
    text = render_text(EMPTY)

    assert text.count("Sin datos") == 2
    assert "Advertencias" in text
    assert "BCV no respondió" in text


def test_embed_contains_rates_and_spreads(snapshot: Snapshot) -> None:
    embed = render_discord_embed(snapshot)
    fields = {field["name"]: field["value"] for field in embed["fields"]}  # type: ignore[index]

    assert embed["title"] == "Reporte de divisas — Venezuela"
    assert embed["color"] == 0x2ECC71
    assert "36.5872" in fields["BCV (oficial)"]
    assert "40.2500" in fields["Binance P2P"]
    assert "+10.01%" in fields["Diferencia vs BCV"]


def test_embed_marks_warnings() -> None:
    embed = render_discord_embed(EMPTY)
    fields = {field["name"]: field["value"] for field in embed["fields"]}  # type: ignore[index]

    assert embed["color"] == 0xE67E22
    assert "BCV no respondió" in fields["Advertencias"]


def test_to_dict(snapshot: Snapshot) -> None:
    data = snapshot.to_dict()

    assert data["fetched_at"] == "2026-11-13T14:30:00+00:00"
    assert data["bcv"] == {"usd": 36.5872, "eur": 42.1056}
    assert data["binance"] == {"buy": 40.25, "sell": 40.9}
    assert data["spread_pct"] == {"buy": 10.01, "sell": 11.79}
    assert data["errors"] == []
