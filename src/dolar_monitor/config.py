from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BCV_URL = "https://www.bcv.org.ve/"
DEFAULT_BINANCE_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
DEFAULT_HTTP_TIMEOUT = 15.0


@dataclass(frozen=True, slots=True)
class Settings:
    bcv_url: str = DEFAULT_BCV_URL
    binance_url: str = DEFAULT_BINANCE_URL
    discord_webhook_url: str | None = None
    http_timeout: float = DEFAULT_HTTP_TIMEOUT

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            bcv_url=os.getenv("BCV_URL") or DEFAULT_BCV_URL,
            binance_url=os.getenv("BINANCE_URL") or DEFAULT_BINANCE_URL,
            discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL") or None,
            http_timeout=_positive_float(os.getenv("HTTP_TIMEOUT"), DEFAULT_HTTP_TIMEOUT),
        )


def _positive_float(raw: str | None, default: float) -> float:
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value > 0 else default
