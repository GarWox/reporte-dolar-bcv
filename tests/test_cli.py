from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

import dolar_monitor.cli as cli
from dolar_monitor.models import Snapshot

EMPTY = Snapshot(
    fetched_at=datetime(2026, 11, 13, 14, 30, tzinfo=timezone.utc),
    errors=("sin conexión",),
)


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "load_dotenv", lambda: None)


def test_prints_text_report(snapshot: Snapshot, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_snapshot", lambda settings: snapshot)

    assert cli.main([]) == 0

    out = capsys.readouterr().out
    assert "BCV (oficial)" in out
    assert "36.5872" in out


def test_prints_json_report(snapshot: Snapshot, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_snapshot", lambda settings: snapshot)

    assert cli.main(["--json"]) == 0

    data = json.loads(capsys.readouterr().out)
    assert data["bcv"]["usd"] == 36.5872
    assert data["spread_pct"]["buy"] == 10.01


def test_returns_error_when_no_data(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_snapshot", lambda settings: EMPTY)

    assert cli.main([]) == 1

    assert "Sin datos" in capsys.readouterr().out


def test_discord_without_webhook_fails(
    snapshot: Snapshot, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    monkeypatch.setattr(cli, "fetch_snapshot", lambda settings: snapshot)

    assert cli.main(["--discord"]) == 2


def test_discord_dry_run_prints_payload(
    snapshot: Snapshot, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/webhook")
    monkeypatch.setattr(cli, "fetch_snapshot", lambda settings: snapshot)
    monkeypatch.setattr(
        cli, "DiscordNotifier", lambda *args, **kwargs: pytest.fail("no debe enviar")
    )

    assert cli.main(["--discord", "--dry-run"]) == 0

    out = capsys.readouterr().out
    assert '"embeds"' in out
    assert "Reporte de divisas" in out
