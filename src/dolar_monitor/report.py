from __future__ import annotations

from .models import Snapshot


def _spread(value: float | None) -> str:
    return "N/D" if value is None else f"{value:+.2f}%"


def render_text(snapshot: Snapshot) -> str:
    lines = [f"Reporte de divisas — {snapshot.fetched_at:%Y-%m-%d %H:%M} UTC", ""]

    lines.append("BCV (oficial)")
    if snapshot.bcv:
        lines.append(f"  USD  {snapshot.bcv.usd:.4f} VES")
        lines.append(f"  EUR  {snapshot.bcv.eur:.4f} VES")
    else:
        lines.append("  Sin datos")

    lines.append("")
    lines.append("Binance P2P (USDT/VES)")
    if snapshot.binance:
        lines.append(f"  Compra  {snapshot.binance.buy:.4f} VES")
        lines.append(f"  Venta   {snapshot.binance.sell:.4f} VES")
    else:
        lines.append("  Sin datos")

    lines.append("")
    lines.append("Diferencia vs BCV")
    lines.append(f"  Compra  {_spread(snapshot.spread_buy)}")
    lines.append(f"  Venta   {_spread(snapshot.spread_sell)}")

    if snapshot.errors:
        lines.append("")
        lines.append("Advertencias")
        lines.extend(f"  - {error}" for error in snapshot.errors)

    return "\n".join(lines)


def _bcv_value(snapshot: Snapshot) -> str:
    if not snapshot.bcv:
        return "Sin datos"
    return f"USD: **{snapshot.bcv.usd:.4f}** VES\nEUR: **{snapshot.bcv.eur:.4f}** VES"


def _binance_value(snapshot: Snapshot) -> str:
    if not snapshot.binance:
        return "Sin datos"
    return (
        f"Compra: **{snapshot.binance.buy:.4f}** VES\n"
        f"Venta: **{snapshot.binance.sell:.4f}** VES"
    )


def render_discord_embed(snapshot: Snapshot) -> dict[str, object]:
    fields: list[dict[str, object]] = [
        {"name": "BCV (oficial)", "value": _bcv_value(snapshot), "inline": True},
        {"name": "Binance P2P", "value": _binance_value(snapshot), "inline": True},
        {
            "name": "Diferencia vs BCV",
            "value": (
                f"Compra: {_spread(snapshot.spread_buy)}\n"
                f"Venta: {_spread(snapshot.spread_sell)}"
            ),
            "inline": False,
        },
    ]
    if snapshot.errors:
        fields.append(
            {
                "name": "Advertencias",
                "value": "\n".join(f"- {error}" for error in snapshot.errors)[:1024],
                "inline": False,
            }
        )

    return {
        "title": "Reporte de divisas — Venezuela",
        "color": 0xE67E22 if snapshot.errors else 0x2ECC71,
        "fields": fields,
        "footer": {"text": "reporte-dolar-bcv"},
        "timestamp": snapshot.fetched_at.isoformat(timespec="seconds"),
    }
