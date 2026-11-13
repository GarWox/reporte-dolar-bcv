from __future__ import annotations

import json

import pytest
import responses

from dolar_monitor.config import Settings
from dolar_monitor.errors import NotificationError
from dolar_monitor.http import HttpClient
from dolar_monitor.notifiers.discord import DiscordNotifier

WEBHOOK = "https://discord.test/webhook"


@responses.activate
def test_send_posts_embed(settings: Settings) -> None:
    responses.post(WEBHOOK, status=204)
    notifier = DiscordNotifier(WEBHOOK, HttpClient(settings, retries=0))

    notifier.send({"embeds": [{"title": "Reporte de divisas"}]})

    assert len(responses.calls) == 1
    body = json.loads(responses.calls[0].request.body)
    assert body["embeds"][0]["title"] == "Reporte de divisas"


@responses.activate
def test_send_wraps_http_errors(settings: Settings) -> None:
    responses.post(WEBHOOK, status=500)
    notifier = DiscordNotifier(WEBHOOK, HttpClient(settings, retries=0))

    with pytest.raises(NotificationError):
        notifier.send({"embeds": []})
