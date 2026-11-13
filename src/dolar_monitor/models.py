from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class BcvRates:
    usd: float
    eur: float


@dataclass(frozen=True, slots=True)
class BinanceRates:
    buy: float
    sell: float


def spread_pct(value: float | None, reference: float | None) -> float | None:
    if value is None or reference is None or reference <= 0:
        return None
    return round((value - reference) / reference * 100, 2)


@dataclass(frozen=True, slots=True)
class Snapshot:
    fetched_at: datetime
    bcv: BcvRates | None = None
    binance: BinanceRates | None = None
    errors: tuple[str, ...] = ()

    @property
    def has_data(self) -> bool:
        return self.bcv is not None or self.binance is not None

    @property
    def spread_buy(self) -> float | None:
        return spread_pct(
            self.binance.buy if self.binance else None,
            self.bcv.usd if self.bcv else None,
        )

    @property
    def spread_sell(self) -> float | None:
        return spread_pct(
            self.binance.sell if self.binance else None,
            self.bcv.usd if self.bcv else None,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "fetched_at": self.fetched_at.isoformat(timespec="seconds"),
            "bcv": {"usd": self.bcv.usd, "eur": self.bcv.eur} if self.bcv else None,
            "binance": (
                {"buy": self.binance.buy, "sell": self.binance.sell} if self.binance else None
            ),
            "spread_pct": {"buy": self.spread_buy, "sell": self.spread_sell},
            "errors": list(self.errors),
        }
