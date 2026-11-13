from __future__ import annotations

import requests

from ..errors import NotificationError
from ..http import HttpClient


class DiscordNotifier:
    def __init__(self, webhook_url: str, client: HttpClient) -> None:
        self._webhook_url = webhook_url
        self._client = client

    def send(self, payload: dict[str, object]) -> None:
        try:
            self._client.post(self._webhook_url, json=payload)
        except requests.RequestException as exc:
            raise NotificationError(f"No se pudo enviar el reporte a Discord: {exc}") from exc
