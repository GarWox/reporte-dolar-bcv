from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from collections.abc import Sequence

from dotenv import load_dotenv

from .config import Settings
from .errors import NotificationError
from .http import HttpClient
from .notifiers.discord import DiscordNotifier
from .report import render_discord_embed, render_text
from .service import fetch_snapshot

logger = logging.getLogger("dolar_monitor")
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def _default_log_level() -> str:
    raw = (os.getenv("LOG_LEVEL") or "INFO").upper()
    return raw if raw in LOG_LEVELS else "INFO"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dolar-monitor",
        description="Reporte de la tasa oficial del BCV y del P2P de Binance para Venezuela.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime el reporte como JSON en lugar de texto.",
    )
    parser.add_argument(
        "--discord",
        action="store_true",
        help="Envía el reporte al webhook de Discord configurado.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra el payload de Discord sin enviarlo.",
    )
    parser.add_argument(
        "--log-level",
        default=_default_log_level(),
        choices=LOG_LEVELS,
        help="Nivel de log (por defecto: LOG_LEVEL o INFO).",
    )
    return parser


def _use_utf8_when_redirected() -> None:
    for stream in (sys.stdout, sys.stderr):
        if stream is None or stream.isatty() or not hasattr(stream, "reconfigure"):
            continue
        stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv: Sequence[str] | None = None) -> int:
    _use_utf8_when_redirected()
    load_dotenv()
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")

    settings = Settings.from_env()
    snapshot = fetch_snapshot(settings)

    if args.json:
        print(json.dumps(snapshot.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_text(snapshot))

    for error in snapshot.errors:
        logger.warning(error)

    if not snapshot.has_data:
        logger.error("No se obtuvo ninguna tasa")
        return 1

    if args.discord:
        if not settings.discord_webhook_url:
            logger.error("Falta DISCORD_WEBHOOK_URL en el entorno")
            return 2
        payload = {"embeds": [render_discord_embed(snapshot)]}
        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        try:
            DiscordNotifier(settings.discord_webhook_url, HttpClient(settings)).send(payload)
        except NotificationError as exc:
            logger.error("%s", exc)
            return 3
        logger.info("Reporte enviado a Discord")

    return 0


if __name__ == "__main__":
    sys.exit(main())
