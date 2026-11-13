from __future__ import annotations


def parse_ves_number(raw: str) -> float:
    """Convierte un número en formato venezolano ("1.234,56") a float."""
    cleaned = raw.replace("\xa0", "").replace(" ", "").strip()
    if not cleaned:
        raise ValueError("valor vacío")
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    return float(cleaned)
